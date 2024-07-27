import os
import re
import pandas as pd
import numpy as np
import tiktoken
from openai import AzureOpenAI
import dotenv

dotenv.load_dotenv()

# 환경 변수 출력
print("AZURE_OPENAI_ENDPOINT:", os.environ.get('AZURE_OPENAI_ENDPOINT'))
print("EMBED_MODEL:", os.environ.get('EMBED_MODEL'))
print("OPENAI_API_VERSION:", os.environ.get('OPENAI_API_VERSION'))
print("AZURE_OPENAI_API_KEY:", os.environ.get('AZURE_OPENAI_API_KEY'))

df = pd.read_csv(os.path.join(os.getcwd(), 'bill_sum_data.csv'))
print(df)

df_bills = df[['text', 'summary', 'title']]
print(df_bills)

pd.options.mode.chained_assignment = None

def normalize_text(s, sep_token=" \n "):
    s = re.sub(r'\s+', ' ', s).strip()
    s = re.sub(r". ,", "", s)
    s = s.replace("..", ".")
    s = s.replace(". .", ".")
    s = s.replace("\n", "")
    s = s.strip()
    return s

df_bills['text'] = df_bills["text"].apply(lambda x: normalize_text(x))

tokenizer = tiktoken.get_encoding("cl100k_base")
df_bills['n_tokens'] = df_bills["text"].apply(lambda x: len(tokenizer.encode(x)))
df_bills = df_bills[df_bills.n_tokens < 8192]
len(df_bills)
print(df_bills)

sample_encode = tokenizer.encode(df_bills.text[0])
decode = tokenizer.decode_tokens_bytes(sample_encode)
print(len(decode))
print(decode)

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

def generate_embeddings(text, model=deployment_name):
    try:
        response = client.embeddings.create(input=[text], model=model)
        return response.data[0].embedding
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        return None

df_bills['ada_v2'] = df_bills["text"].apply(lambda x: generate_embeddings(x, model=deployment_name))

print(df_bills)

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def get_embedding(text, model=deployment_name):
    try:
        response = client.embeddings.create(input=[text], model=model)
        return response.data[0].embedding
    except Exception as e:
        print(f"Error getting embedding: {e}")
        return None

def search_docs(df, user_query, top_n=4, to_print=True):
    embedding = get_embedding(user_query, model=deployment_name)
    if embedding is None:
        return None

    df["similarities"] = df.ada_v2.apply(lambda x: cosine_similarity(x, embedding) if x is not None else -1)

    res = df.sort_values("similarities", ascending=False).head(top_n)
    return res

res = search_docs(df_bills, "Can I get information on cable company tax revenue?", top_n=4)
if res is not None:
    print(res["summary"].iloc[0])
else:
    print("No results found")
