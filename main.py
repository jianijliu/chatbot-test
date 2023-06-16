import streamlit as st
import pandas as pd

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

# prompt = PromptTemplate(
#    input_variables = [user_text], template = template, )

# def load_LLM():
#    llm = OpenAI(temparature=.5)
#    return llm

# llm = load_LLM()



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



##################################################################################################





#### part 2. Chat part


import openai
from streamlit_chat import message

## reference: https://github.com/AI-Yash/st-chat

## authenrization
openai.api_key = st.secrets["api_secret"]

## create chatbot
def generate_response(prompt):
    completions = openai.Completion.create(
        engine = 'text-davinci-003',
        prompt = prompt,
        max_tokens = 4000,
        n = 1,
        stop = None,
        temparature = 0.5,
    )
    message = completions.choices[0].text
    return message

## text show on screen
message("Hello RYX!")
message("Hi~ ChatGPT!", is_user=True)

## store conversation
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []

## user type in:
def get_text():
    input_text = st.text_area(label="", placeholder="Type here to ask ChatGPT...", key='chat')
    return input_text
user_input = get_text()

## GPT generates response
if user_input:
    gpt_output = generate_response(user_input)
    # store the output
    st.session_state.past.append(user_input)
    st.session_state.generated.append(gpt_output)
    # save the record to dataframe


if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')





## save the conversation


#if user_input:
#    prompt_with_input = prompt.format(user_text=user_input)
#    gpt_answer = llm(prompt_with_input)
#    st.write(gpt_answer)


#df = pd.DataFrame({'user': [user_input], 'gpt': [gpt_answer]})
#df.to_csv('/Users/joeyliu/Desktop/ChatGPT/ChatBot/user1.csv', index=False)


















