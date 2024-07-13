import ollama
from config import Config
from  query_qa_pairs import query

model = Config['model']

qa_template = """
You are an expert on my purchased microwave oven. I will provide you with a set of questions about microwave ovens, 
and I would like you to answer them using the following context:

Context:
{context}

Please provide concise and informative answers question below, using the provided context in the Q&A format.

Question:
{question}

Answer:
"""

def llm_response(question, context):
    prompt = qa_template.format(question=question, context=context)
    response = ollama.generate(model, prompt)['response']
    return response.strip()

def to_context(documents):
    return '\n\n'.join([ doc for _, _, doc in documents])

if __name__ == "__main__":
    question = input("What's your question for your microwave oven ? ")
    documents = query(question)
    context = to_context(documents)    
    response = llm_response(question, context)
    print(f"The answer to your question is:\n{response}")