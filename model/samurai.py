from vanna.chromadb import ChromaDB_VectorStore
from vanna.bedrock import Bedrock_Converse
from botocore.exceptions import ClientError
import json
import time
from customsf import CustomSF
from dotenv import load_dotenv
import plotly
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from model.vanai_prompts import prompts

import os

load_dotenv()


class Samurai(Bedrock_Converse, ChromaDB_VectorStore, CustomSF):
    def __init__(self, client=None, config=None):
        ChromaDB_VectorStore.__init__(
            self,
            config={
                "n_results_sql": 20,
                "n_results_documentation": 10,
                "n_results_ddl": 40,
            },
        )
        Bedrock_Converse.__init__(
            self,
            client=client,
            config={
                "modelId": "anthropic.claude-3-sonnet-20240229-v1:0",
                "initial_prompt": prompts,
            },
        )
        # Change the path
        rsa_key_path = os.environ.get(
            "SNOWFLAKE_RSA_KEY_PATH", "/Users/sainath/Desktop/rsa_key.p8"
        )
        CustomSF.__init__(self, key_path=rsa_key_path)

    def merge_consecutive_messages(self, messages):
        merged_messages = []
        for message in messages:
            if merged_messages and merged_messages[-1]["role"] == message["role"]:
                merged_messages[-1]["content"].append(
                    {
                        "text": " ".join(
                            [
                                merged_messages[-1]["content"][-1]["text"],
                                message["content"][0]["text"],
                            ]
                        )
                    }
                )
            else:
                merged_messages.append(message)
        return merged_messages

    def submit_prompt_v2(
        self, first_prompt, previous_messages, prompt, **kwargs
    ) -> str:
        inference_config = {
            "temperature": self.temperature,
            "maxTokens": self.max_tokens,
        }
        additional_model_fields = {
            "top_p": 1,  # setting top_p value for nucleus sampling
        }

        system_message = None
        no_system_prompt = []
        for prompt_message in first_prompt:
            role = prompt_message["role"]
            if role == "system":
                system_message = prompt_message["content"]
            else:
                no_system_prompt.append(
                    {"role": role, "content": [{"text": prompt_message["content"]}]}
                )
        if previous_messages:
            for message in previous_messages:
                if message["role"] == "user":
                    no_system_prompt.append(
                        {"role": "user", "content": [{"text": message["content"]}]}
                    )
                else:
                    no_system_prompt.append(
                        {"role": "assistant", "content": [{"text": message["content"]}]}
                    )
        if prompt:
            no_system_prompt.append({"role": "user", "content": [{"text": prompt}]})
        no_system_prompt = self.merge_consecutive_messages(no_system_prompt)
        converse_api_params = {
            "modelId": self.model,
            "messages": no_system_prompt,
            "inferenceConfig": inference_config,
            "additionalModelRequestFields": additional_model_fields,
        }

        if system_message:
            converse_api_params["system"] = [{"text": system_message}]

        try:
            response = self.client.converse(**converse_api_params)
            text_content = response["output"]["message"]["content"][0]["text"]
            cur_time = time.strftime("%Y%m%d-%H%M%S")
            filename = f"logs/{cur_time}.json"

            def safe_open_w(path):
                """Open "path" for writing, creating any parent directories as needed."""
                os.makedirs(os.path.dirname(path), exist_ok=True)
                return open(path, "w")

            with safe_open_w(filename) as f:
                f.write(
                    json.dumps(
                        {
                            "messages": converse_api_params["messages"],
                            "response": text_content,
                            "system": converse_api_params["system"],
                        }
                    )
                )
            return text_content
        except ClientError as err:
            message = err.response["Error"]["Message"]
            raise Exception(f"A Bedrock client error occurred: {message}")

    def generate_sql_v2(
        self, previous_messages, question, allow_llm_to_see_data=False, **kwargs
    ) -> str:
        """
        Example:
        ```python
        vn.generate_sql("What are the top 10 customers by sales?")
        ```

        Uses the LLM to generate a SQL query that answers a question. It runs the following methods:

        - [`get_similar_question_sql`][vanna.base.base.VannaBase.get_similar_question_sql]

        - [`get_related_ddl`][vanna.base.base.VannaBase.get_related_ddl]

        - [`get_related_documentation`][vanna.base.base.VannaBase.get_related_documentation]

        - [`get_sql_prompt`][vanna.base.base.VannaBase.get_sql_prompt]

        - [`submit_prompt`][vanna.base.base.VannaBase.submit_prompt]


        Args:
            question (str): The question to generate a SQL query for.
            allow_llm_to_see_data (bool): Whether to allow the LLM to see the data (for the purposes of introspecting the data to generate the final SQL).

        Returns:
            str: The SQL query that answers the question.
        """
        first_message = question
        if previous_messages and len(previous_messages) > 0:
            first_message = previous_messages[0]["content"]

        if self.config is not None:
            initial_prompt = self.config.get("initial_prompt", None)
        else:
            initial_prompt = None
        question_sql_list = self.get_similar_question_sql(first_message, **kwargs)
        ddl_list = self.get_related_ddl(first_message, **kwargs)
        doc_list = self.get_related_documentation(first_message, **kwargs)
        first_prompt = self.get_sql_prompt(
            initial_prompt=initial_prompt,
            question=first_message,
            question_sql_list=question_sql_list,
            ddl_list=ddl_list,
            doc_list=doc_list,
            **kwargs,
        )
        # self.log(title="SQL Prompt", message=first_prompt)
        if previous_messages:
            previous_messages = previous_messages[1:]
        llm_response = self.submit_prompt_v2(
            first_prompt, previous_messages, question, **kwargs
        )
        # self.log(title="LLM Response", message=llm_response)

        if "intermediate_sql" in llm_response:
            if not allow_llm_to_see_data:
                return "The LLM is not allowed to see the data in your database. Your question requires database introspection to generate the necessary SQL. Please set allow_llm_to_see_data=True to enable this."

            if allow_llm_to_see_data:
                intermediate_sql = self.extract_sql(llm_response)

                try:
                    self.log(title="Running Intermediate SQL", message=intermediate_sql)
                    df = self.run_sql(intermediate_sql)

                    prompt = self.get_sql_prompt(
                        initial_prompt=initial_prompt,
                        question=first_message,
                        question_sql_list=question_sql_list,
                        ddl_list=ddl_list,
                        doc_list=doc_list
                        + [
                            f"The following is a pandas DataFrame with the results of the intermediate SQL query {intermediate_sql}: \n"
                            + df.to_markdown()
                        ],
                        **kwargs,
                    )
                    # self.log(title="Final SQL Prompt", message=first_prompt)
                    llm_response = self.submit_prompt_v2(
                        prompt, previous_messages, question, **kwargs
                    )
                    # self.log(title="LLM Response", message=llm_response)
                except Exception as e:
                    if not previous_messages:
                        previous_messages = []
                    previous_messages.append({"role": "user", "content": first_message})
                    previous_messages.append(
                        {"role": "assistant", "content": intermediate_sql}
                    )
                    prompt = self.get_sql_prompt(
                        initial_prompt=initial_prompt,
                        question=first_message,
                        question_sql_list=question_sql_list,
                        ddl_list=ddl_list,
                        doc_list=doc_list,
                        **kwargs,
                    )
                    llm_response = self.submit_prompt_v2(
                        prompt,
                        previous_messages,
                        f"Got the following error {e}, can you recheck syntax?",
                        **kwargs,
                    )
                    return f"Error running intermediate SQL: {e}"

        return self.extract_sql(llm_response)

    def get_plotly_figure_v2(
        self, plotly_code: str, df: pd.DataFrame, dark_mode: bool = True
    ) -> plotly.graph_objs.Figure:
        """
        **Example:**
        ```python
        fig = vn.get_plotly_figure(
            plotly_code="fig = px.bar(df, x='name', y='salary')",
            df=df
        )
        fig.show()
        ```
        Get a Plotly figure from a dataframe and Plotly code.

        Args:
            df (pd.DataFrame): The dataframe to use.
            plotly_code (str): The Plotly code to use.

        Returns:
            plotly.graph_objs.Figure: The Plotly figure.
        """
        ldict = {"df": df, "px": px, "go": go}
        try:
            exec(plotly_code, globals(), ldict)

            fig = ldict.get("fig", None)
        except Exception as e:
            # Inspect data types
            numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
            categorical_cols = df.select_dtypes(
                include=["object", "category"]
            ).columns.tolist()
            if len(numeric_cols) == 1 and len(categorical_cols) == 0:
                return None
            elif len(numeric_cols) == 0 and len(categorical_cols) == 1:
                return None
            elif len(numeric_cols) == 0 and len(categorical_cols) == 0:
                return None
            # Decision-making for plot type
            elif len(numeric_cols) >= 2 and len(categorical_cols) == 0:
                # Use the first two numeric columns for a scatter plot
                fig = px.scatter(df, x=numeric_cols[0], y=numeric_cols[1])
            elif len(numeric_cols) == 1 and len(categorical_cols) >= 1:
                # Use a bar plot if there's one numeric and one categorical column
                fig = px.bar(df, x=categorical_cols[0], y=numeric_cols[0])
                fig.update_traces(marker_color="#00b899")
                for i, row in df.iterrows():
                    fig.add_annotation(
                        x=row[categorical_cols[0]],
                        y=row[numeric_cols[0]],
                        text=f"{row[numeric_cols[0]]}",
                        showarrow=True,
                        arrowhead=2,
                        ax=0,
                        ay=-30,
                    )
            elif (
                len(categorical_cols) >= 1
                and df[categorical_cols[0]].nunique() < 10
                and len(numeric_cols) == 0
            ):
                # Use a pie chart for categorical data with fewer unique values
                fig = px.pie(df, names=categorical_cols[0])
            elif len(categorical_cols) == 1 and len(numeric_cols) >= 1:
                # Use a bar plot for multiple numeric columns with one categorical column
                fig = px.bar(df, x=categorical_cols[0], y=numeric_cols)
                fig.update_layout(
                    barmode="relative", xaxis={"categoryorder": "category ascending"}
                )
            else:
                # Default to a simple line plot if above conditions are not met
                fig = px.line(df)

        if fig is None:
            return None

        if dark_mode:
            fig.update_layout(template="plotly_white")

        return fig

    def get_sql_prompt(
        self,
        initial_prompt : str,
        question: str,
        question_sql_list: list,
        ddl_list: list,
        doc_list: list,
        **kwargs,
    ):
        """
        Example:
        ```python
        vn.get_sql_prompt(
            question="What are the top 10 customers by sales?",
            question_sql_list=[{"question": "What are the top 10 customers by sales?", "sql": "SELECT * FROM customers ORDER BY sales DESC LIMIT 10"}],
            ddl_list=["CREATE TABLE customers (id INT, name TEXT, sales DECIMAL)"],
            doc_list=["The customers table contains information about customers and their sales."],
        )

        ```

        This method is used to generate a prompt for the LLM to generate SQL.

        Args:
            question (str): The question to generate SQL for.
            question_sql_list (list): A list of questions and their corresponding SQL statements.
            ddl_list (list): A list of DDL statements.
            doc_list (list): A list of documentation.

        Returns:
            any: The prompt for the LLM to generate SQL.
        """

        if initial_prompt is None:
            initial_prompt = f"You are a {self.dialect} expert. " + \
            "Please help to generate a SQL query to answer the question. Your response should ONLY be based on the given context and follow the response guidelines and format instructions. "

        if self.static_documentation != "":
            doc_list.append(self.static_documentation)

        initial_prompt = self.add_documentation_to_prompt(
            initial_prompt, doc_list, max_tokens=self.max_tokens
        )

        initial_prompt += (
            "===Response Guidelines \n"
            "1. If the provided context is sufficient, please generate a valid snowflake SQL query without any explanations for the question. \n"
            "2. If the provided context is almost sufficient but requires knowledge of a specific string in a particular column, please generate an intermediate SQL query to find the distinct strings in that column. Prepend the query with a comment saying intermediate_sql \n"
            "3. If the provided context is insufficient, please explain why it can't be generated. \n"
            "4. Please use the most relevant table(s). \n"
            "5. If the question has been asked and answered before, please repeat the answer exactly as it was given before. \n"
        )
        message_log = [self.system_message(initial_prompt)]
        ddl_prompt = self.add_ddl_to_prompt(
            "", ddl_list, max_tokens=self.max_tokens
        )
        message_log.append(self.user_message(ddl_prompt))
        message_log.append(self.assistant_message("Acknowledged schema, now please send your query"))

        for example in question_sql_list:
            if example is None:
                print("example is None")
            else:
                if example is not None and "question" in example and "sql" in example:
                    message_log.append(self.user_message(example["question"]))
                    message_log.append(self.assistant_message(example["sql"]))

        message_log.append(self.user_message(question))

        return message_log