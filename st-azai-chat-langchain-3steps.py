import os
# from langchain_community.chat_models import AzureChatOpenAI
from langchain_openai import AzureChatOpenAI
from langchain.schema import HumanMessage
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser

# Load environment variables from .env file
load_dotenv()

# Set up OpenAI client
api_key = os.getenv('AZURE_OPENAI_API_KEY')
azure_endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
api_version = os.getenv('OPENAI_API_VERSION')
deployment_name = os.getenv('CHAT_COMPLETIONS_MODEL')

# 1) 프롬프트
template = """
당신은 영어를 가르치는 10년차 영어 선생님입니다. 주제에 대해 [FORMAT]으로 영어 회화를 작성해 주세요.
주제: {agenda}
FORMAT:
- 영어 회화:
- 한글 해석:
"""
prompt = PromptTemplate.from_template(template)

# 2) 모델
# Initialize an instance of AzureChatOpenAI using the specified settings
llm = AzureChatOpenAI(
    azure_endpoint=azure_endpoint,
    openai_api_version=api_version,
    deployment_name=deployment_name,
    openai_api_key=api_key,
    openai_api_type="azure",
)

# result = llm([HumanMessage(content="Write me a poem")]) -->변경: llm.invoke()
# result = llm.invoke("Write me a poem")  --> 위의 방식이 invoke 방식으로 변경

# 3) 출력
# 문자열 출력 파서를 초기화합니다.
output_parser = StrOutputParser()
#
# 프롬프트, 모델, 출력 파서를 연결하여 처리 체인을 구성합니다.
chain = prompt | llm | output_parser
#
print(chain.invoke({"agenda": "저는 식당에 가서 음식을 주문하고 싶어요"}))
