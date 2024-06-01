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

# Currently Chat Completion API have the following versions available: 2023-03-15-preview
api_version = os.environ['OPENAI_API_VERSION']

client = AzureOpenAI(
    api_key=api_key,
    azure_endpoint=azure_endpoint,
    api_version=api_version
)

# Define a function to get the summary from OpenAI
def get_summary():
    try:
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that rearrange sentences"},
                {"role": "user", "content": f"Rearrange the following sentences: {st.session_state.user_input}"}
            ]
        )

        # Display the response
        st.session_state.summary = response.choices[0].message.content

    except openai.AuthenticationError as e:
        st.session_state.summary = f"OpenAI API returned an Authentication Error: {e}"

    except openai.APIConnectionError as e:
        st.session_state.summary = f"Failed to connect to OpenAI API: {e}"

    except openai.BadRequestError as e:
        st.session_state.summary = f"Invalid Request Error: {e}"

    except openai.RateLimitError as e:
        st.session_state.summary = f"OpenAI API request exceeded rate limit: {e}"

    except openai.InternalServerError as e:
        st.session_state.summary = f"Service Unavailable: {e}"

    except openai.APITimeoutError as e:
        st.session_state.summary = f"Request timed out: {e}"

    except openai.APIError as e:
        st.session_state.summary = f"OpenAI API returned an API Error: {e}"

    except Exception as e:
        st.session_state.summary = f"An exception has occurred: {e}"

# Initialize session state variables
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""

if 'summary' not in st.session_state:
    st.session_state.summary = ""

# Main layout
st.title("Sentence Rearrangement App")

# User input for text to summarize
st.text_area("Enter sentences to rearrange::", key='user_input', height=200, on_change=get_summary)

# Display the summary
if st.session_state.summary:
    st.write("**Summary:**")
    st.write(st.session_state.summary)
