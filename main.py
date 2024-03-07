import streamlit as st
import openai
from streamlit_chat import message
from google.oauth2 import service_account
from gsheetsdb import connect
import gspread
import pandas as pd
from datetime import datetime
import socket
    
#### Demo: https://chatbot-test-jiani.streamlit.app/

#### part 0. main page setting
st.set_page_config(page_title='Optima', page_icon=':robot:')
col1, col2, col3 = st.columns([1,6,1])
with col1:
    st.write("")
with col2:
    st.image("logo-optima.png", width=500)   # lumina.png
with col3:
    st.write("")
# st.image(image='lumina.png', width=500)
st.markdown('\n')

#### part 1. Instruction (sidebar)
# st.sidebar.title("任务须知")
st.sidebar.title("Instructions")
counter_placeholder = st.sidebar.empty()
st.sidebar.info('''
    You will be asked to complete **one task** with the Optima platform. \n 
    Details of the task can be found on the Qualtrics page. \n 
    Please ensure that you **do not close the Qualtrics and the Optima platform pages** while completing the task. \n
    You can type in your Prolific ID and press Enter to initiate this service: \n 
    ''')

#您需要在Optima平台上完成**一个搜索任务**，在开始之前，请认真阅读以下内容: \n
#1. 在完成任务的过程中**请不要关闭Credamo的页面**; \n
#2. 使用自己的**实验编号**登陆Optima平台，请确保填写正确，否则可能影响实验报酬的发放; \n
#3. 在完成任务期间**仅使用Optima平台**，请勿使用任何其他设备或工具辅助完成; \n
#4. 请避免依靠您自己的知识来完成任务，应该充分**利用Optima平台**上搜索到的结果完成任务。\n

user_id = st.sidebar.text_input("Prolific ID...") # disabled=st.session_state.disabled, on_change=disable
# user_id = st.sidebar.text_input("在此填写实验编号...")

#### part 2. Chat part
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

# Connect to Google Sheets (reference: https://docs.streamlit.io/knowledge-base/tutorials/databases/private-gsheet)
# Create a connection object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=["https://www.googleapis.com/auth/spreadsheets",],
)
conn = connect(credentials=credentials)
client = gspread.authorize(credentials)

# Read Google Sheets
sheet_url = st.secrets["private_gsheets_url"]
sheet = client.open_by_url(sheet_url).sheet1   # select a worksheet
    
# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"
    
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
image_url = "https://api.dicebear.com/6.x/icons/svg?seed=Mimi&icon=flower1&scale=85&"  #  Rocky
# image_url = "https://api.dicebear.com/7.x/micah/svg?seed=Mimi&baseColor=f9c9b6&glasses=round&hairColor=6bd9e9&mouth=smile&backgroundColor=b6e3f4,transparent&scale=110"
for message in st.session_state.messages:
    role = message["role"]
    if role not in ["assistant"]:
        with st.chat_message("user"):
            st.markdown(message["content"])
    else:
        with st.chat_message("assistant", avatar=image_url):
            st.markdown(message["content"])

if user_id:
    # Accept user input
    if prompt := st.chat_input(placeholder="ask Optima"):
        input_time = str(datetime.now())
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Display assistant response in chat message container
        with st.chat_message("assistant", avatar=image_url):
            message_placeholder = st.empty()
            full_response = ""
            for response in openai.ChatCompletion.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            ):
                full_response += response.choices[0].delta.get("content", "")
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        output_time = str(datetime.now())
        row = [user_id, input_time, prompt, output_time, full_response]
        sheet.insert_row(row)

else:
    st.markdown("\n")
    # st.markdown("<h3 style='text-align: center;'> 感谢您参与本次实验! <br> 请先仔细阅读侧边栏中的任务须知，<br> 并输入自己的实验编号以开启实验! </h3>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>Please read instructions in the sidebar carefully and \n type in your Prolific ID to initiate this service!</h2>", unsafe_allow_html=True)
    # st.markdown("Please read instructions in the sidebar carefully and type in your participant ID first!")
