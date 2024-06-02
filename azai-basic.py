# import os module & the OpenAI Python library for calling the OpenAI API
import os
import openai
from openai import AzureOpenAI
import dotenv
dotenv.load_dotenv()

# Setting up the deployment name
deployment_name = os.environ['COMPLETIONS_MODEL']

# The API key for your Azure OpenAI resource.
api_key = os.environ["AZURE_OPENAI_API_KEY"]

# The base URL for your Azure OpenAI resource. e.g. "https://<your resource name>.openai.azure.com"
azure_endpoint = os.environ['AZURE_OPENAI_ENDPOINT']

# Currently Chat Completion API have the following versions available: 2024-05-01-preview
api_version = os.environ['OPENAI_API_VERSION']

client = AzureOpenAI(
  api_key=api_key,
  azure_endpoint=azure_endpoint,
  api_version=api_version
)

try:
    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Who won the world series in 2020?"}
        ]
    )

    # print the response
    print(response.choices[0].message.content)

except openai.AuthenticationError as e:
    # Handle Authentication error here, e.g. invalid API key
    print(f"OpenAI API returned an Authentication Error: {e}")

except openai.APIConnectionError as e:
    # Handle connection error here
    print(f"Failed to connect to OpenAI API: {e}")

except openai.BadRequestError as e:
    # Handle connection error here
    print(f"Invalid Request Error: {e}")

except openai.RateLimitError as e:
    # Handle rate limit error
    print(f"OpenAI API request exceeded rate limit: {e}")

except openai.InternalServerError as e:
    # Handle Service Unavailable error
    print(f"Service Unavailable: {e}")

except openai.APITimeoutError as e:
    # Handle request timeout
    print(f"Request timed out: {e}")

except openai.APIError as e:
    # Handle API error here, e.g. retry or log
    print(f"OpenAI API returned an API Error: {e}")

except:
    # Handles all other exceptions
    print("An exception has occured.")