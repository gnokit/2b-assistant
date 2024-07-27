import streamlit as st
from typing import Iterable
from config import Config
from query_qa_pairs import query_to_context
from llm_rag_response import stream_rag_response, to_chat_history
from expand_prompt import expand_prompt

# print(f"Configuration: {Config}")

witch_avatar = "👧🏻"
user_avatar = "😊"
model = Config["model"]
welcome_message = f"""
Hi there! I'm the Microwave Witch {witch_avatar}. 
I know all about your microwave oven. What question do you have for me? I'm here to help!
"""

st.set_page_config(
    page_title=f"Microwave Witch {witch_avatar}",
)
st.title(f"Microwave Witch {witch_avatar}")
st.image("images/microwave.png")


def generate_reply(query_text, chat_history, context) -> Iterable:
    """Generate a reply to the user's query using RAG."""
    for chunk in stream_rag_response(
        query_text=query_text, chat_history=chat_history, context=context
    ):
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
    with st.chat_message(
        message["role"],
        avatar=user_avatar if message["role"] == "user" else witch_avatar,
    ):
        st.markdown(message["content"])

if prompt := st.chat_input():
    # Add user's query to chat history.
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Write user's input to gui
    with st.chat_message("user", avatar=user_avatar):
        st.markdown(prompt)

    # Generate reply from Ollama model and write to gui.
    with st.chat_message("assistant", avatar=witch_avatar):
        with st.spinner("Casting...🪄"):
            # Expanded user queries into more specific, context-aware questions
            expanded = expand_prompt(st.session_state.messages)
            # Perform similary search of query_text and return the top_k documents as context
            context = query_to_context(query_text=expanded)
            # Use chat history to assist the response
            chat_history = to_chat_history(st.session_state.messages)
            # Generate helpful, accurate, and user-friendly responses to customer inquiries
            response = st.write_stream(generate_reply(prompt, chat_history, context))
            # Write debugging information. 🔍
            with st.sidebar:
                st.title("DEBUG")
                st.markdown(f"**Expanded:**\n\n{expanded}\n\n**Context:**\n\n{context}")

    # Add reply to chat history.
    st.session_state.messages.append({"role": "assistant", "content": response})
