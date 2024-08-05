import streamlit as st
from typing import Iterable
from config import config
from query_qa_pairs import query_to_context
from llm_rag_response import stream_rag_response, to_chat_history
from expand_prompt import expand_prompt
from talking_appliance import select_appliance

# print(f"Configuration: {Config}")

witch_avatar = "👧🏻"
user_avatar = "😊"
model = config.MODEL
welcome_message = config.WELCOME_MESSAGE

st.set_page_config(
    page_title=f"2.6B: Your Appliance Knowledge Hub 📚🔧",
)
st.title(f"2.6B - Your Appliance Knowledge Hub 📚🔧")
st.image("images/26-b.png")


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
            # Use chat history to assist the response
            chat_history = to_chat_history(st.session_state.messages)
            # Expanded user queries into more specific, context-aware questions
            expanded = expand_prompt(st.session_state.messages)
            # select talking appliance from chat history
            appliance = select_appliance(prompt, chat_history=chat_history)
            # Prevent llm only returns one word
            for app in config.APPLICANTS:
                if app in appliance:
                    appliance = app
                    break
            
            # Perform similary search of query_text and return the top_k documents as context
            context = (
                query_to_context(appliance, query_text=expanded)
                if appliance != "unknown"
                else "N/A"
            )
            # Generate helpful, accurate, and user-friendly responses to customer inquiries
            response = st.write_stream(generate_reply(expanded, context))
            # Write debugging information. 🔍
            with st.sidebar:
                st.title("DEBUG")
                st.markdown(
                    f"**Appliance:**\n\n{appliance}\n\n**Expanded:**\n\n{expanded}\n\n**Context:**\n\n{context}"
                )

    # Add reply to chat history.
    st.session_state.messages.append({"role": "assistant", "content": response})
