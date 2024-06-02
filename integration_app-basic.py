import os
import openai
from openai import AzureOpenAI
import dotenv
import streamlit as st

# Load environment variables
dotenv.load_dotenv()

# Initialize AzureOpenAI client
deployment_name = os.environ['CHAT_COMPLETIONS_MODEL']
api_key = os.environ["AZURE_OPENAI_API_KEY"]
azure_endpoint = os.environ['AZURE_OPENAI_ENDPOINT']
api_version = os.environ['OPENAI_API_VERSION']
client = AzureOpenAI(api_key=api_key, azure_endpoint=azure_endpoint, api_version=api_version)

# Initialize session state variables
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""

if 'target_language' not in st.session_state:
    st.session_state.target_language = ""

# Function to get completion from OpenAI
def get_completion(user_input, assistant_description, user_prompt):
    try:
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": assistant_description},
                {"role": "user", "content": user_prompt.format(user_input, st.session_state.target_language)}
            ]
        )
        return response.choices[0].message.content
    except openai.APIError as e:
        return f"OpenAI API Error: {e}"
    except Exception as e:
        return f"An exception has occurred: {e}"

# Sidebar navigation
st.sidebar.title("Navigation")
selected_option = st.sidebar.radio("Go to:", ["Chat", "Summary", "Translate", "Rewrite"])

# Main content based on selected option
st.title("Azure OpenAI App")

if selected_option == "Chat":
    st.header("Chat")
    user_input = st.text_input("Enter your message:")
    if st.button("Send"):
        if user_input:
            response = get_completion(user_input, "You are a helpful assistant.", "{}")
            st.write("**Response:**")
            st.write(response)
        else:
            st.warning("Please enter a message.")
elif selected_option == "Summary":
    st.header("Summary")
    user_input = st.text_area("Enter text to summarize:", height=200)
    if st.button("Summarize"):
        if user_input:
            response = get_completion(user_input, "You are a helpful assistant that summarizes text with the form of ({keyword}): {content}",
                                       "Summarize the following text: {}")
            st.write("**Summary:**")
            st.write(response)
        else:
            st.warning("Please enter text to summarize.")
elif selected_option == "Translate":
    st.header("Translate")
    user_input = st.text_area("Enter text to translate:", height=200)
    target_language = st.text_input("Enter target language (e.g., Spanish, French, German):")
    if st.button("Translate"):
        if user_input and target_language:
            st.session_state.target_language = target_language
            response = get_completion(user_input, "You are a helpful assistant that translates text.",
                                       "Translate the following text to only {}: {}")
            st.write("**Translation:**")
            st.write(response)
        else:
            st.warning("Please enter text to translate and target language.")
elif selected_option == "Rewrite":
    st.header("Rewrite")
    user_input = st.text_area("Enter sentences to rewrite:", height=200)
    if st.button("Rewrite"):
        if user_input:
            response = get_completion(user_input, "You are a helpful assistant that rearranges sentences.",
                                       "Rearrange the following sentences: {}")
            st.write("**Rewritten Text:**")
            st.write(response)
        else:
            st.warning("Please enter sentences to rewrite.")
