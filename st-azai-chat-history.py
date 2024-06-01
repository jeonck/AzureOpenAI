# https://github.com/Azure-Samples/openai/blob/main/Basic_Samples/Chat/chatGPT_managing_conversation.ipynb
import os
import openai
from openai import AzureOpenAI
import tiktoken
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up OpenAI client
deployment_name = os.getenv('CHAT_COMPLETIONS_MODEL')
azure_endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
api_key = os.getenv('AZURE_OPENAI_API_KEY')
api_version = os.getenv('OPENAI_API_VERSION')

base_system_message = "You are a helpful assistant."

system_message = f"{base_system_message.strip()}"
print(system_message)

client = AzureOpenAI(
    api_key=api_key,
    azure_endpoint=azure_endpoint,
    api_version=api_version
)

import tiktoken

def num_tokens_from_messages(messages, model="gpt-4o"):
    encoding = tiktoken.encoding_for_model(model)
    num_tokens = 0
    for message in messages:
        num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":  # if there's a name, the role is omitted
                num_tokens += -1  # role is always required and always 1 token
    num_tokens += 2  # every reply is primed with <im_start>assistant
    return num_tokens

# Defining a function to send the prompt to the ChatGPT model
# More info : https://learn.microsoft.com/en-us/azure/cognitive-services/openai/how-to/chatgpt?pivots=programming-language-chat-completions
def send_message(messages, model_name, max_response_tokens=500):
    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        temperature=0.5,
        max_tokens=max_response_tokens,
        top_p=0.9,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return response.choices[0].message.content

# Defining a function to print out the conversation in a readable format
def print_conversation(messages):
    for message in messages:
        print(f"[{message['role'].upper()}]")
        print(message['content'])
        print()

# This is the first user message that will be sent to the model. Feel free to update this.
user_message = "I want to write a blog post about the impact of AI on the future of work."

# Create the list of messages. role can be either "user" or "assistant"
messages=[
    {"role": "system", "content": system_message},
    {"role": "user", "name":"example_user", "content": user_message}
]

token_count = num_tokens_from_messages(messages)
print(f"Token count: {token_count}")

max_response_tokens = 500

response = send_message(messages, deployment_name, max_response_tokens)
messages.append({"role": "assistant", "content": response})

print_conversation(messages)