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

MAX_SQL_RETRY = 5

class Samurai(Bedrock_Converse, ChromaDB_VectorStore, CustomSF):
    def __init__(self, client=None, config=None):
        ChromaDB_VectorStore.__init__(
            self,
            config={
                "n_results_sql": 10,
                "n_results_documentation": 10,
                "n_results_ddl": 150,
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
        total_length = 0
        for nmps in no_system_prompt:
            if len(nmps["content"]) == 1:
                cnt = nmps["content"][0]["text"]
            else:
                cnt = nmps["content"]
            total_length += self.str_to_approx_token_count(cnt)
        print("TOTAL_TOKENS_LENGTH", total_length)
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

                sql_retry_remaining = MAX_SQL_RETRY
                intermediate_sql_prompt = question
                while sql_retry_remaining > 0:
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
                            prompt, previous_messages, intermediate_sql_prompt, **kwargs
                        )
                        break
                        # self.log(title="LLM Response", message=llm_response)
                    except Exception as e:
                        print("ERROR running Intermediate sql", e)
                        if not previous_messages:
                            previous_messages = []
                        previous_messages.append(self.user_message(first_message))
                        previous_messages.append(self.assistant_message(first_message))

                        intermediate_sql_prompt =f"Got the following error {e}, can you recheck syntax? - do not add comments to the sql query",

                        sql_retry_remaining -= 1
                        if sql_retry_remaining == 0:
                            return f"Error running intermediate SQL: {e}"

        return self.extract_sql(llm_response)

    def generate_plotly_code_v2(
        self,
        previous_message,
        question: str = None,
        sql: str = None,
        df_metadata: str = None,
        **kwargs,
    ) -> str:
        if question is not None:
            system_msg = f"The following is a pandas DataFrame that contains the results of the query that answers the question the user asked: '{question}'"
        else:
            system_msg = "The following is a pandas DataFrame "

        if sql is not None:
            system_msg += f"\n\nThe DataFrame was produced using this query: {sql}\n\n"

        system_msg += f"The following is information about the resulting pandas DataFrame 'df': \n{df_metadata}"

        prompt = "Can you generate the Python plotly code to chart the results of the dataframe? Assume the data is in a pandas dataframe called 'df'.If we have only one row in our dataframe, don't create any charts. If one of the column_name is like actor_id or any id then don't generate chart. If one column value looks like date and we have multiple numerical columns in it and one of the numerical values columns all values are less than 1 then create a dual axis line chart. If we have only categorical columns in our dataframe, don't create any charts.If we have one categorical columns and its value present in it looks like date or timestamp and other as columns are numerical then create line charts where categorical column is x axis. If there is only one categorical or one numerical variable or one row, do not create charts - return an empty plotty code. If one categorical columns with date values and one numerical columns are present, create line charts. If two categorical and one numerical columns are present, create stacked bar charts. If we have one categorical columns and multiple numerical columns then create line charts or bar charts. Use colour #00B899 if plotting a single variable as line or bar. Use Indicator with automatic alignment for all charts. Use these colour also whenever needed - (#004E2D,#007A56,#00B899,#6BCDB6,#A8E0D3,#DCF3EE,#6D313F,#A73F4B,#D45967,#E895A1,#F2BDC6,#F8E5EB). Respond with only Python code. Do not answer with any explanations -- just the code."

        # plotly_code = self.submit_prompt(message_log, kwargs=kwargs)
        plotly_code = self.submit_prompt_v2(
            first_prompt=[self.system_message(system_msg)],
            previous_messages=previous_message,
            prompt=prompt,
            kwargs=kwargs,
        )

        return self._sanitize_plotly_code(self._extract_python_code(plotly_code))

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
            if plotly_code == "":
                raise Exception("No plotly code provided")

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
        initial_prompt: str,
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
            initial_prompt = (
                f"You are a {self.dialect} expert. "
                + "Please help to generate a SQL query to answer the question. Your response should ONLY be based on the given context and follow the response guidelines and format instructions. "
            )

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
        ddl_prompts = self.add_ddl_to_prompt_v2(ddl_list, max_tokens=1400)
        message_log += ddl_prompts

        for example in question_sql_list:
            if example is None:
                print("example is None")
            else:
                if example is not None and "question" in example and "sql" in example:
                    message_log.append(self.user_message(example["question"]))
                    message_log.append(self.assistant_message(example["sql"]))

        message_log.append(self.user_message(question))

        return message_log

    def add_ddl_to_prompt_v2(self, ddl_list: list[str], max_tokens: int = 14000):
        message_log_sequence = []
        current_prompt = "\n===Tables \n"
        current_token_length = 0
        for ddl in ddl_list:
            total_token_count = self.str_to_approx_token_count(
                current_prompt
            ) + self.str_to_approx_token_count(ddl)
            if total_token_count < max_tokens:
                current_prompt += f"{ddl}\n\n"
                current_token_length += total_token_count
            else:
                message_log_sequence.append(self.user_message(current_prompt))
                message_log_sequence.append(
                    self.assistant_message(
                        "Acknowledged schema, now please send your query or send more schemas"
                    )
                )
                current_prompt = "\n===Tables \n"
                current_prompt += f"{ddl}\n\n"
                current_token_length = total_token_count
        if current_prompt != "\n===Tables \n":
            message_log_sequence.append(self.user_message(current_prompt))
            message_log_sequence.append(
                self.assistant_message(
                    "Acknowledged schema, now please send your query or send more schemas"
                )
            )

        return message_log_sequence
