import os
import openai
from openai import AzureOpenAI
import dotenv
import streamlit as st

# Load environment variables
dotenv.load_dotenv()

# Setting up the deployment name
deployment_name = os.environ['COMPLETIONS_MODEL']

# The API key for your Azure OpenAI resource.
api_key = os.environ["AZURE_OPENAI_API_KEY"]

# The base URL for your Azure OpenAI resource. e.g. "https://<your resource name>.openai.azure.com"
azure_endpoint = os.environ['AZURE_OPENAI_ENDPOINT']

# Currently Chat Completion API have the following versions available: 2023-03-15-preview
api_version = os.environ['OPENAI_API_VERSION']

client = AzureOpenAI(
    api_key=api_key,
    azure_endpoint=azure_endpoint,
    api_version=api_version
)

# Define a function to get the answer from OpenAI
def get_answer():
    try:
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": st.session_state.user_input}
            ]
        )

        # Display the response
        st.session_state.answer = response.choices[0].message.content

    except openai.AuthenticationError as e:
        st.session_state.answer = f"OpenAI API returned an Authentication Error: {e}"

    except openai.APIConnectionError as e:
        st.session_state.answer = f"Failed to connect to OpenAI API: {e}"

    except openai.BadRequestError as e:
        st.session_state.answer = f"Invalid Request Error: {e}"

    except openai.RateLimitError as e:
        st.session_state.answer = f"OpenAI API request exceeded rate limit: {e}"

    except openai.InternalServerError as e:
        st.session_state.answer = f"Service Unavailable: {e}"

    except openai.APITimeoutError as e:
        st.session_state.answer = f"Request timed out: {e}"

    except openai.APIError as e:
        st.session_state.answer = f"OpenAI API returned an API Error: {e}"

    except Exception as e:
        st.session_state.answer = f"An exception has occurred: {e}"

# Initialize session state variables
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""

if 'answer' not in st.session_state:
    st.session_state.answer = ""

# Main layout
st.title("Azure OpenAI Chat Completion Example")

# User input with on_change callback
st.text_input("Enter your question:", key='user_input', on_change=get_answer)

# Display the answer
if st.session_state.answer:
    st.write("**Answer:**")
    st.write(st.session_state.answer)