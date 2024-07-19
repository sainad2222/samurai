from vanna.bedrock.bedrock_converse import boto3
from vanna.chromadb import ChromaDB_VectorStore
from vanna.bedrock import Bedrock_Converse
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


session = boto3.Session()
boto3_bedrock = boto3.client(service_name="bedrock-runtime")

vn = Samurai(client=boto3_bedrock)


# print(vn.ask("Hello"))
vn.connect_to_snowflake
vn.connect_to_snowflake_v2()
vn.run_sql()
