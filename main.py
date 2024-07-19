from vanna.bedrock.bedrock_converse import boto3
from vanna.chromadb import ChromaDB_VectorStore
from vanna.bedrock import Bedrock_Converse
from utils import bedrock
from dotenv import load_dotenv

import os
import sys

load_dotenv()


module_path = ".."
sys.path.append(os.path.abspath(module_path))


class Samurai(Bedrock_Converse, ChromaDB_VectorStore):
    def __init__(self, client=None, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        Bedrock_Converse.__init__(
            self,
            client=client,
            config={"modelId": "anthropic.claude-3-sonnet-20240229-v1:0"},
        )


# os.environ["AWS_PROFILE"] = "<YOUR_PROFILE>"

# boto3_bedrock = bedrock.get_bedrock_client(
#     assumed_role=os.environ.get("BEDROCK_ASSUME_ROLE", None),
#     region=os.environ.get("AWS_DEFAULT_REGION", None),
# )
session = boto3.Session()
boto3_bedrock = boto3.client(service_name="bedrock-runtime")

vn = Samurai(client=boto3_bedrock)


print(vn.ask("Hello"))
