import streamlit as st
import ollama
from typing import Dict, Iterable
from config import Config
from query_qa_pairs import query_to_context

model = Config["model"]
welcome_message = """
Hi there! I'm the Microwave Witch 🧙‍♀️. 
I know all about your microwave oven. What question do you have for me? I'm here to help!
"""
sys_prompt_prefix = """
You are an AI expert of a household microwave oven.
If context section exists below, use it to answer the question.
"""


def get_sys_prompt(context=""):
    """Generate a system prompt for Ollama model."""
    context_prompt = "" if context is None else "\n\nContext: " + context
    return sys_prompt_prefix + context_prompt


def generate_reply(chat_history: Dict) -> Iterable:
    """Generate a reply to the user's query."""
    # Get user's query from the last message in chat history.
    query_text = chat_history[-1]["content"]
    # Get context for the query from source.
    context = query_to_context(query_text=query_text)
    # Inject context into system prompt.
    chat_history[0] = {"role": "system", "content": get_sys_prompt(context=context)}
    # Generate reply from Ollama model.
    responses = ollama.chat(model, messages=chat_history, stream=True)
    for response in responses:
        yield response["message"]["content"]

def init_messages():
    """Initialize chat history with system prompt and welcome message."""
    return [
        {"role": "system", "content": get_sys_prompt()},
        {"role": "assistant", "content": welcome_message},
    ]


st.title("Microwave Witch 🧙‍♀️")

if "messages" not in st.session_state:
    # Initialize chat history with system prompt and welcome message.
    st.session_state.messages = init_messages()

for message in st.session_state.messages:
    # Display messages from chat history. Ignore system messages.
    if message["role"] != "system":
        st.markdown(message["content"])

if prompt := st.chat_input():
    # Add user's query to chat history.
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Write user's input to gui
    with st.chat_message("user"):
        st.markdown(prompt)
    # Generate reply from Ollama model and write to gui.
    with st.chat_message("assistant"):
        response = st.write_stream(generate_reply(st.session_state.messages))
    # Add reply to chat history.
    st.session_state.messages.append({"role": "assistant", "content": response})
