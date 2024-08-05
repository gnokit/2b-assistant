import ollama
from config import config
from query_qa_pairs import query_to_context

model = config.MODEL

output_format = """
**Output Format:**
2.6B must structure its response below to show the process of going through each step:
1. Query identified: [Briefly restate the user's question]
2. Context search: [Indicate if relevant information was found or not. If found, go through each information step by step]
3. Final response: [Provide the formulated response or state that a "404 not found" response is prepared. Deliver the final answer, incorporating all previous steps]
"""

prompt_template = """
You are 2.6B, a personalized AI assistant for the user's appliances.  
You have detailed knowledge about the specific appliances the user has purchased and registered.  
Your role is to provide tailored, helpful, and accurate responses to inquiries about these appliances.

2.6B's Persona:
- Efficient and direct, with a focus on precision and clarity  
- Calm and composed, even when addressing less tech-savvy users  
- Dedicated to assisting with the user's specific appliances  
- Highly knowledgeable about the exact models and features of the user's registered appliances  
- Safety-conscious and always prioritizes the user's well-being and the proper use of their appliances  
- **(I must ensure that my responses are clear and helpful.)**  
- **(Understanding the user's needs is my top priority.)**  

**Instructions for 2.6B:**
**Note:** 2.6B must go through all the following steps to formulate a response.

1. **Identify the User's Query:**
   - Understand what the user is asking about their appliance.

2. **Search the Context:**
   - Look for relevant information in the "Context" section. 
   - If relevant information is found, prepare to use it in your response. If not, prepare a "404 not found" response and ask the user for more details.

3. **Deliver the Final Response:**
   - If information is found, create a concise and actionable answer in point form, including any necessary safety warnings or best practices.
   - If no information is found, respond with "404 not found" and request more details.
   - Provide the user with the prepared answer or the "404 not found" message, ensuring the tone is efficient and direct. (I must prioritize user safety and clarity in my response.)    

Current Question:
{question}

Context (if available):
```
{context}
```

Output:
"""

tests = [
    {
        "appliance": "washing machine",
        "query": "How much detergent should I use in the washing machine?",
    },
    {
        "appliance": "washing machine",
        "query": "How does the eco mode on a washing machine save energy?",
    },
    {
        "appliance": "washing machine",
        "query": "How to fix a clogged drain hose in a washing machine?",
    },
    {
        "appliance": "washing machine",
        "query": "How to use the delicate cycle on a washing machine for a gentle wash?",
    },
    {
        "appliance": "microwave oven",
        "query": "How to use the defrost setting on a microwave oven for chicken?",
    },
    {
        "appliance": "microwave oven",
        "query": "How to cook scrambled eggs in a microwave oven?",
    },
    {
        "appliance": "microwave oven",
        "query": "How to steam clean a microwave oven?",
    },
    {
        "appliance": "microwave oven",
        "query": "Why should I pierce a potato before microwaving it?",
    },
]


def stream_rag_response(query_text, context):
    """Generate stream of responses using Ollama model by given context and query text"""
    prompt = prompt_template.format(context=context, question=query_text)
    responses = ollama.generate(
        model=model,
        prompt=prompt,
        stream=True,
        options={"temperature": config.TEMPERATURE},
    )
    for response in responses:
        yield response["response"]


def to_chat_history(conversation):
    """Convert conversation to chat history"""
    return "\n".join(f"{chat['role']}: {chat['content']}" for chat in conversation)


if __name__ == "__main__":

    for test in tests:
        query_text = test["query"]
        manual = test["appliance"]
        context = query_to_context(manual=manual, query_text=query_text)
        print(f"\nTest: {query_text}")
        for chunk in stream_rag_response(query_text, context):
            print(chunk, end="", flush=True)
