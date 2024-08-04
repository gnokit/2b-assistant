import ollama
import logging
from config import config, create_logger

logger = create_logger("expand_prompt")

model = config.MODEL

prompt_template = """
You are an AI assistant designed to expand user queries into more specific, context-aware questions.
Your task is to transform the user's latest input into a detailed question 
that captures their intent and incorporates relevant context from recent conversations.

Recent conversation context:
```
{context}
```

User's latest input:
{user_input}

Please transform the user's input into a specific, detailed question that:
1. Incorporates relevant information from the conversation context
2. Clarifies any ambiguous terms or references (like "it" or "this")
3. Is formatted as a complete, grammatically correct question
4. Maintains the original intent of the user's input
5. Response transformed question only without prefix, explanation or comments

Transformed question:
"""


def to_context(chat_history):
    return "\n".join(
        [
            f"{'AI: ' if chat['role'] == 'assistant' else 'Human: '}: {chat['content']}\n"
            for chat in chat_history
        ]
    )


def expand_prompt(chat_history, limit=5):
    user_input = chat_history[-1]["content"]
    context = to_context(chat_history[-limit:-1])
    prompt = prompt_template.format(context=context, user_input=user_input)
    logger.debug(f"Prompt: {prompt}")
    response = ollama.generate(model, prompt)
    return response["response"].strip()


messages = [
    {"content": "hi", "role": "user"},
    {
        "content": "Hi! It's nice to meet you. Is there something I can help you with or would you like to chat?",
        "role": "assistant",
    },
    {"content": "what's common function of oven?", "role": "user"},
    {
        "content": "Ovens are commonly used for cooking and heating food. Here are some of the most common functions of an oven:\n\n1. **Baking**: Ovens are great for baking cakes, cookies, bread, and pastries.\n2. **Roasting**: Ovens are perfect for roasting meats, vegetables, and potatoes to perfection.\n3. **Broiling**: Ovens can be used to broil meats, fish, and vegetables to give them a crispy, caramelized exterior.\n4. **Heating**: Ovens can be used to simply heat up food, such as warming leftovers or reheating cooked meals.\n5. **Cooking**: Ovens can be used to cook a variety of dishes, including casseroles, lasagnas, and other savory dishes.\n6. **Defrosting**: Some ovens have a defrost setting that allows you to defrost frozen foods quickly and safely.\n7. **Proofing**: Ovens can be used to proof yeast dough, allowing it to rise to the perfect consistency.\n\nThese are just a few examples of the many functions of an oven. Ovens are incredibly versatile and can be used for a wide range of cooking tasks!",
        "role": "assistant",
    },
    {
        "content": "baking?",  # this is the same as the previous message's content
        "role": "user",
    },    
]

if __name__ == "__main__":
    logger.setLevel(logging.DEBUG)
    print(expand_prompt(chat_history=messages))
