from vanna.bedrock.bedrock_converse import boto3
from vanna.chromadb import ChromaDB_VectorStore
from vanna.bedrock import Bedrock_Converse
from botocore.exceptions import ClientError
from customsf import CustomSF
from dotenv import load_dotenv

import os
import sys

load_dotenv()


module_path = ".."
sys.path.append(os.path.abspath(module_path))


class Samurai(Bedrock_Converse, ChromaDB_VectorStore, CustomSF):
    def __init__(self, client=None, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        Bedrock_Converse.__init__(
            self,
            client=client,
            config={"modelId": "anthropic.claude-3-sonnet-20240229-v1:0"},
        )
        # Change the path
        rsa_key_path = os.environ.get(
            "SNOWFLAKE_RSA_KEY_PATH", "/Users/sainath/Desktop/rsa_key.p8"
        )
        CustomSF.__init__(self, key_path=rsa_key_path)

    def submit_prompt_v2(self, previous_messages, prompt, **kwargs) -> str:
        inference_config = {
            "temperature": self.temperature,
            "maxTokens": self.max_tokens,
        }
        additional_model_fields = {
            "top_p": 1,  # setting top_p value for nucleus sampling
        }

        no_system_prompt = []
        for message in previous_messages:
            if message["role"] == "user":
                no_system_prompt.append(
                    {"role": "user", "content": [{"text": message["content"]}]}
                )
            else:
                no_system_prompt.append(
                    {"role": "assistant", "content": [{"text": message["content"]}]}
                )

        system_message = None
        for prompt_message in prompt:
            role = prompt_message["role"]
            if role == "system":
                system_message = prompt_message["content"]
            else:
                no_system_prompt.append(
                    {"role": role, "content": [{"text": prompt_message["content"]}]}
                )

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
            return text_content
        except ClientError as err:
            message = err.response["Error"]["Message"]
            raise Exception(f"A Bedrock client error occurred: {message}")
