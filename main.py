import streamlit as st
import openai
from streamlit_chat import message

## load in to terminal
# cd /Users/joeyliu/Desktop/ChatGPT/ChatBot
# ls
# streamlit run main.py

#### part 1. Introduction part

# introduction message
st.set_page_config(page_title='ChatBot 1', page_icon=':robot:')
st.header("🤖️You are chating with ChatGPT")
st.markdown('Thank you for participating this research!  \n '
            'You will be asked to have a conversation with ChatGPT to **generate a recipe**. Following the chat, you’ll be redirected back to the survey to answer a few final questions and receive your payment code. ')

st.markdown('\n')
st.markdown("**Please paste your participation ID:**")
def get_text():
    input_text = st.text_area(label="", placeholder="Participation ID...", key='text1')
    return input_text
user_id = get_text()

st.markdown('---')
st.markdown('\n')
st.markdown('\n')
st.markdown('\n')


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

# St the GPT-3 api key
openai.api_key = st.secrets["API_KEY"]

# -----------------------------------
def generate_response(prompt):
    completions = openai.Completion.create (
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    message = completions.choices[0].text
    return message

if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []

## text show on screen
message("Hello RYX!")
message("Hi~ ChatGPT!", is_user=True)

## get text
st.markdown("\n")
st.markdown("**You can ask ChatGPT how to make a pancake:**")

def get_text():
    input_text = st.text_input("You: ", "", key="input")
    return input_text 

user_input = get_text()

if user_input:
    output = generate_response(user_input)
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')














