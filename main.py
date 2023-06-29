import streamlit as st
import openai
from streamlit_chat import message
from google.oauth2 import service_account
from gsheetsdb import connect
import gspread
import pandas as pd
from datetime import datetime

#### part 1. Introduction part
# instruction message
st.set_page_config(page_title='ChatBot-Jiani', page_icon=':robot:')
st.header("🤖️You are chating with ChatGPT")
st.markdown('You will be asked to have a conversation with ChatGPT to **generate a recipe**. Following the chat, you’ll be redirected back to the survey to answer a few final questions and receive your payment code. ')
st.markdown('\n')
st.sidebar.title("Thank you for participating this research!")
counter_placeholder = st.sidebar.empty()
# ask for participation id
counter_placeholder.markdown("**Please paste your participation ID:**")
def get_text():
    input_text = st.sidebar.text_area(label="", placeholder="Participation ID...", key='text1')
    return input_text
user_id = get_text()

#### part 2. Chat part
# reference: https://github.com/AI-Yash/st-chat

## prompt engieering
template = """
    Below is a question that target creating a recipe.
    Your goal is to: 
    - Ask her preference
    - Ask the occasion of this meal
    - Create a specific meal for this occasion according to her preference
    
    Below is the question.
    QUESTION: {user_text} 
    
    YOUR RESPONSE: 
"""

# Set the GPT-3 api key
openai.api_key = st.secrets["API_KEY"]

# Connect to Google Sheets
# reference: https://docs.streamlit.io/knowledge-base/tutorials/databases/private-gsheet
# Create a connection object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
    ],
)
conn = connect(credentials=credentials)
client = gspread.authorize(credentials)

# Write in Google Sheets
# First, Reading from Google Sheets
sheet_url = st.secrets["private_gsheets_url"]
# df_database = pd.read_csv(sheet_url, on_bad_lines='skip')
sheet = client.open_by_url(sheet_url).sheet1  # select a worksheet

# generate a response
def generate_response(prompt):
    st.session_state['messages'].append({"role": "user", "content": prompt})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=st.session_state['messages']
    )
    response = completion.choices[0].message.content
    st.session_state['messages'].append({"role": "assistant", "content": response})
    # print(st.session_state['messages'])
    return response
    
# Initialise session state variables
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
            
# container for chat history
response_container = st.container()
# container for text box
container = st.container()


if user_id:
    ## text show on screen
    message("Hi! ChatGPT", is_user=True)
    message("Hello! RYX")
    
    with container:
        with st.form(key='my_form', clear_on_submit=True):
            user_input = st.text_area("You can ask ChatGPT how to make a pancake:", key='input', height=100)
            submit_button = st.form_submit_button(label='Send')

        if submit_button and user_input:
            input_time = str(datetime.now())
            output = generate_response(user_input)
            st.session_state['past'].append(user_input)
            st.session_state['generated'].append(output)
            # insert a new row
            output_time = str(datetime.now())
            row = [user_id, input_time, user_input, output_time, output]
            sheet.insert_row(row)
        
    if st.session_state['generated']:
        with response_container:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
                message(st.session_state["generated"][i], key=str(i))
else:
    st.markdown("**Please type in participant ID first!**")
    st.markdown("\n")

