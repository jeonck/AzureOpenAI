import os
import openai
from openai import AzureOpenAI
import dotenv
import streamlit as st

# Load environment variables
dotenv.load_dotenv()

# Setting up the deployment name
deployment_name = os.environ['CHAT_COMPLETIONS_MODEL']

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

# Define a function to get the answer from OpenAI
def get_translation():
    try:
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that translates text."},
                {"role": "user", "content": f"Translate the following text to only {st.session_state.target_language}: {st.session_state.user_input}"}
            ]
        )

        # Display the response
        st.session_state.translation = response.choices[0].message.content

    except openai.AuthenticationError as e:
        st.session_state.translation = f"OpenAI API returned an Authentication Error: {e}"

    except openai.APIConnectionError as e:
        st.session_state.translation = f"Failed to connect to OpenAI API: {e}"

    except openai.BadRequestError as e:
        st.session_state.translation = f"Invalid Request Error: {e}"

    except openai.RateLimitError as e:
        st.session_state.translation = f"OpenAI API request exceeded rate limit: {e}"

    except openai.InternalServerError as e:
        st.session_state.translation = f"Service Unavailable: {e}"

    except openai.APITimeoutError as e:
        st.session_state.translation = f"Request timed out: {e}"

    except openai.APIError as e:
        st.session_state.translation = f"OpenAI API returned an API Error: {e}"

    except Exception as e:
        st.session_state.translation = f"An exception has occurred: {e}"

# Initialize session state variables
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""

if 'target_language' not in st.session_state:
    st.session_state.target_language = "English"

if 'translation' not in st.session_state:
    st.session_state.translation = ""

# Main layout
st.title("Azure OpenAI Translation App")

# User input for text to translate
st.text_input("Enter text to translate:", key='user_input', on_change=get_translation)

# User input for target language
st.text_input("Enter target language (e.g., Spanish, French, German):", key='target_language', on_change=get_translation)

# Display the translation
if st.session_state.translation:
    st.write("**Translation:**")
    st.write(st.session_state.translation)
