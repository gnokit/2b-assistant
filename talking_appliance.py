import ollama
from config import Config
from llm_rag_response import to_chat_history

model = Config["model"]
appliances = "\n".join(f"- {app}" for app in Config["appliances"].split(","))

appliance_selection_prompt = """
You are an AI assistant tasked with determining which household appliance is being discussed in a conversation.
Your goal is to analyze the chat history and current question to identify the relevant appliance.

Instructions:
1. Carefully read through the chat history and the current question.
2. Look for keywords, context clues, or direct mentions of any household appliance.
3. If multiple appliances are mentioned, determine which one is the main focus of the current question.
4. If no specific appliance is explicitly mentioned, use context clues to infer which appliance is most likely being discussed.
5. If it's impossible to determine a specific appliance or if the conversation is about an appliance not listed below, respond with "UNKNOWN".

Currently supported appliances:
{appliances}

Your response should be exactly one word from the list above or "UNKNOWN".

Chat History:
{chat_history}

Current Question:
{question}

Determine the appliance being discussed and respond with only one word:
"""

samples = [
    {
        "role": "assistant",
        "content": "\nHi there! I'm the Appliance Helper 🧙\u200d♀️. \nI know all about your appliances. What question do you have for me? I'm here to help!\n",
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

def select_appliance(question, chat_history):
    prompt = appliance_selection_prompt.format(
        question=question,
        chat_history=chat_history,
        appliances=appliances
    )
    response = ollama.generate(model=model, prompt=prompt)
    return response["response"].strip().lower()

if __name__ == "__main__":
    query_text = "i see"  
    chat_history = to_chat_history(samples)
    print(select_appliance(query_text, chat_history=chat_history))