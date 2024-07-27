from langchain_openai import AzureOpenAIEmbeddings
from openai import AzureOpenAI
import dotenv
import os

dotenv.load_dotenv()
# 환경 변수 설정
deployment_name = os.environ['EMBED_MODEL']
api_key = os.environ["AZURE_OPENAI_API_KEY"]
azure_endpoint = os.environ['AZURE_OPENAI_ENDPOINT']
api_version = os.environ['OPENAI_API_VERSION']

client = AzureOpenAI(
    api_key=api_key,
    api_version=api_version,
    azure_endpoint=azure_endpoint
)
openai = AzureOpenAIEmbeddings(model="text-embedding-3-large")


