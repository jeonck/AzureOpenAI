### 패키지 
from langchain_community.document_loaders import TextLoader
from langchain_openai import AzureOpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma

from openai import AzureOpenAI
import dotenv
import os

dotenv.load_dotenv()

### .env 예시 
AZURE_OPENAI_API_KEY="ㅇㅇㅇ"
AZURE_OPENAI_ENDPOINT="https://ㅇㅇㅇ.openai.azure.com/"
#CHAT_MODEL="deployment-sand-aop"  # 4o
#CHAT_MODEL="deployment-35turbo-instruct-sand-aop"
CHAT_MODEL="deployment-35turbo-16k-sand-aop"
OPENAI_API_VERSION="2024-02-01"
EMBED_MODEL="deployment-embed3-sand-aop"
###
환경변수 설정 후에
# 환경 변수 설정
deployment_name = os.environ['EMBED_MODEL']
api_key = os.environ["AZURE_OPENAI_API_KEY"]
azure_endpoint = os.environ['AZURE_OPENAI_ENDPOINT']
api_version = os.environ['OPENAI_API_VERSION']
---
### 
import os
import dotenv

from langchain_openai import AzureOpenAI

# Load environment variables from .env file
dotenv.load_dotenv(dotenv_path='./.env')

# Create an instance of the AzureChatOpenAI class using Azure OpenAI
llm = AzureOpenAI(
    deployment_name=os.getenv("OPENAI_DEPLOYMENT_NAME"),
    temperature=0.7,
    openai_api_version="2023-05-15")

### 

### 일반 chat
client = AzureOpenAI(
    api_key=api_key,
    azure_endpoint=azure_endpoint,
    api_version=api_version
)

### langchain
# Initialize an instance of AzureChatOpenAI using the specified settings
llm = AzureChatOpenAI(
    azure_endpoint=azure_endpoint,
    openai_api_version=api_version,
    deployment_name=deployment_name,
    openai_api_key=api_key,
    openai_api_type="azure",
)
### 이미지 해석
client = AzureOpenAI(
    api_key=api_key,
    api_version=api_version,
    base_url=f"{azure_endpoint}/openai/deployments/{deployment_name}"
)
### 임베딩 다룰 때
client = AzureOpenAI(
    api_key=api_key,
    api_version=api_version,
    azure_endpoint=azure_endpoint
)
### dall-e 배포 후 사용 방식
client = AzureOpenAI(
    api_version="2024-02-01",
    api_key=api_key,
    azure_endpoint=azure_endpoint
)
### assistant 활용
client = AzureOpenAI(
    api_key=api_key,
    api_version=api_version,
    azure_endpoint=azure_endpoint
)
