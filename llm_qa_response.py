import ollama
from config import Config
from query_qa_pairs import query_to_context

model = Config["model"]

prompt_template = """
You are an AI expert of a household microwave oven.
If context section in QA pair format exists below, use it to answer the question.
Otherwise use general knowledge to answer the following question.

Context:
{context}

Question:
{question}

Answer:
"""


def llm_qa_response(query_text, context):
    """Generate response using Ollama model by given context and query text"""
    prompt = prompt_template.format(context=context, question=query_text)
    ollm_response = ollama.generate(model=model, prompt=prompt)
    return ollm_response["response"].strip()


def stream_qa_response(query_text, context):
    """Generate stream of responses using Ollama model by given context and query text"""
    prompt = prompt_template.format(context=context, question=query_text)
    responses = ollama.generate(model=model, prompt=prompt, stream=True)
    for response in responses:
        yield response["response"]


if __name__ == "__main__":
    query_text = input("What's your question? ")
    context = query_to_context(query_text)
    for chunk in stream_qa_response(query_text, context):
        print(chunk, end="", flush=True)
