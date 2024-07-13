import streamlit as st
import ollama
from typing import Dict, Iterable
from config import Config
from query_qa_pairs import query_to_context

model = Config['model']
welcome_message = """
Hi there! I'm the Microwave Witch 🧙‍♀️. 
I know all about your microwave oven. What question do you have for me? I'm here to help!
"""
sys_prompt_prefix = """
You are an AI expert of a household microwave oven.
If context section exists below, use it to answer the question.
"""   

def get_sys_prompt(context = ""): 
    context_prompt = "" if context is None else "\n\nContext: " + context
    return sys_prompt_prefix + context_prompt    

def generate_reply(chat_history: Dict) -> Iterable:
    query_text = chat_history[-1]['content']
    context = query_to_context(query_text=query_text)
    chat_history[0] = {"role": "system", "content": get_sys_prompt(context=context)}    
    responses = ollama.chat(model, messages=chat_history, stream=True)
    for response in responses:
        yield response['message']['content']
        
def init_messages():
    return [
        {"role": "system", "content": get_sys_prompt()},
        {"role": "assistant", "content": welcome_message}
    ]        

st.title("Microwave Witch 🧙‍♀️")

if "messages" not in st.session_state:
    st.session_state.messages = init_messages()

for message in st.session_state.messages:    
    if message["role"] != "system":    
        st.markdown(message["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        response = st.write_stream(generate_reply(st.session_state.messages))
        
    st.session_state.messages.append(
        {"role": "assistant", "content": response})