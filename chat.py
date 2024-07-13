import streamlit as st
import ollama
from typing import Dict, Iterable
from config import Config

model = Config['model']

def fetch_ollama_replies(chat_history: Dict) -> Iterable:
    responses = ollama.chat(model, messages=chat_history, stream=True)
    for response in responses:
        yield response['message']['content']

st.title("Chat with " + model)

if "selected_model" not in st.session_state:
    st.session_state.selected_model = ""
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How can I help you?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
   
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        response = st.write_stream(fetch_ollama_replies(st.session_state.messages))
        
    st.session_state.messages.append(
        {"role": "assistant", "content": response})