import streamlit as st
from typing import Dict, Iterable
from config import Config
from query_qa_pairs import query_to_context
from llm_rag_response import stream_rag_response

model = Config["model"]
welcome_message = """
Hi there! I'm the Microwave Witch 🧙‍♀️. 
I know all about your microwave oven. What question do you have for me? I'm here to help!
"""


def generate_reply(chat_history: Dict) -> Iterable:
    """Generate a reply to the user's query."""
    # Get user's query from the last message in chat history.
    query_text = chat_history[-1]["content"]
    # Get context for the query from source.
    context = query_to_context(query_text=query_text)
    # Stream the RAG response from the model.
    for chunk in stream_rag_response(query_text=query_text, context=context):
        yield chunk


def init_messages():
    """Initialize chat history with system prompt and welcome message."""
    return [
        {"role": "assistant", "content": welcome_message},
    ]


st.title("Microwave Witch 🧙‍♀️")

if "messages" not in st.session_state:
    # Initialize chat history with system prompt and welcome message.
    st.session_state.messages = init_messages()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
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
