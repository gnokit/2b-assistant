import ollama
from config import Config
from query_qa_pairs import query_to_context

model = Config["model"]

prompt_template = """
You are an AI customer service representative specializing in household microwave ovens.
Your role is to provide helpful, accurate, and user-friendly responses to customer inquiries.

Instructions:
1. If a "Context" section containing question-answer (QA) pairs is provided below, use this information as your primary source to answer the user's question.
2. If the exact question isn't in the context, use the most relevant information from the provided QA pairs to formulate your answer.
3. If no context is provided or the context doesn't contain relevant information, use your general knowledge about microwave ovens to answer the question.
4. Always maintain a polite, professional, and helpful tone in your responses.
5. If you're unsure about any aspect of the answer, acknowledge this and suggest the customer contact human support for more detailed information.
6. Provide concise yet comprehensive answers, focusing on practical and actionable information.
7. If appropriate, include safety warnings or best practices in your responses.

Remember:
- Prioritize user safety in all your responses.
- If the question is outside your expertise or not related to microwave ovens, politely redirect the customer to the appropriate resource or support channel.
- If a question requires technical repair advice beyond basic troubleshooting, advise the customer to seek professional service to ensure safety and proper handling.

Please answer the following question based on these guidelines:
{question}

Context (if available):
{context}

Response:
"""


def rag_response(query_text, context):
    """Generate response using Ollama model by given context and query text"""
    prompt = prompt_template.format(context=context, question=query_text)
    ollm_response = ollama.generate(model=model, prompt=prompt)
    return ollm_response["response"].strip()


def stream_rag_response(query_text, context):
    """Generate stream of responses using Ollama model by given context and query text"""
    prompt = prompt_template.format(context=context, question=query_text)
    responses = ollama.generate(model=model, prompt=prompt, stream=True)
    for response in responses:
        yield response["response"]


samples = [
    {
        "role": "assistant",
        "content": "\nHi there! I'm the Microwave Witch 🧙\u200d♀️. \nI know all about your microwave oven. What question do you have for me? I'm here to help!\n",
    },
    {"role": "user", "content": "hi what's my oven model number?"},
    {
        "role": "assistant",
        "content": " The model numbers for your microwave oven are NN-ST25JW, NN-ST25JB, or NN-ST25JW (mentioned in the context you provided). Please check the identification label on your oven to confirm.",
    },
    {"role": "user", "content": "oh how big it is?"},
    {
        "role": "assistant",
        "content": " The size of a household microwave oven varies depending on the model. However, a common size for a standard countertop microwave is around 20 inches (51 cm) wide, 17 inches (43 cm) deep, and 16 inches (40 cm) tall. But please refer to the specifications of your particular model for exact dimensions.",
    },
]


def to_chat_history(conversation):
    """Convert conversation to chat history"""
    pass


if __name__ == "__main__":
    query_text = input("What's your question? ")
    context = query_to_context(query_text)
    for chunk in stream_rag_response(query_text, context):
        print(chunk, end="", flush=True)
