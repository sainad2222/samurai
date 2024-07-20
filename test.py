import boto3


from dotenv import load_dotenv
from model.samurai import Samurai

load_dotenv()

session = boto3.Session()
boto3_bedrock = boto3.client(service_name="bedrock-runtime")

vn = Samurai(client=boto3_bedrock)
vn.generate_sql("Who are our top 10 users?")
