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

st.set_page_config(
    page_title="Microwave Witch 🧙‍♀️",
)
st.title("Microwave Witch 🧙‍♀️")


def generate_reply(query_text, context) -> Iterable:
    """Generate a reply to the user's query using RAG."""
    for chunk in stream_rag_response(query_text=query_text, context=context):
        yield chunk


def init_messages():
    """Initialize chat history with system prompt and welcome message."""
    return [
        {"role": "assistant", "content": welcome_message},
    ]

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
        context = query_to_context(query_text=prompt)
        with st.spinner("Casting...🪄"):
            response = st.write_stream(generate_reply(prompt, context))
            # Add context to the message if it's not empty. 📖
            if len(context) > 0:
                st.text("📝", help=context)

    # Add reply to chat history.
    st.session_state.messages.append({"role": "assistant", "content": response})
