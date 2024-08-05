import ollama
from config import config
from llm_rag_response import to_chat_history

model = config.MODEL
appliances = ",".join(app for app in config.APPLICANTS)

appliance_selection_prompt = """
You are an AI assistant tasked with determining which household appliance is being discussed in a conversation.
Your goal is to analyze the chat history and current question to identify the relevant appliance.

Instructions:
1. Carefully read through the chat history and the current question.
2. Look for keywords, context clues, or direct mentions of any household appliance.
3. If multiple appliances are mentioned, determine which one is the main focus of the current question.
4. If no specific appliance is explicitly mentioned, use context clues to infer which appliance is most likely being discussed.
5. For queries that don't explicitly mention an appliance, consider common tasks associated with each appliance:
    Washing machine: cleaning clothes, removing stains, wash cycles, detergents, fabric care
    Microwave oven: heating food, defrosting, cooking times, food preparation, reheating
6. If it's impossible to determine a specific appliance or if the conversation is about an appliance not listed above, respond with "unknown".

Currently supported appliances delimited by comma character:
{appliances}

Your response should be exactly appliance from the list above or "unknown".

Chat History:
{chat_history}

Current Question:
{question}

Determine the appliance being discussed and respond the appliance only:
"""


history = [
    {
        "role": "assistant",
        "content": config.WELCOME_MESSAGE,
    }
]

tests = [
    {
        "appliance": "microwave oven",
        "history": history,
        "query": "How long should I reheat pizza?",
    },
    {
        "appliance": "washing machine",
        "history": history,
        "query": "Can I wash silk in the machine?",
    },
    {
        "appliance": "microwave oven",
        "history": history,
        "query": "What's the best way to defrost chicken?",
    },
    {
        "appliance": "washing machine",
        "history": history,
        "query": "How do I clean the detergent drawer?",
    },
    {
        "appliance": "microwave oven",
        "history": history,
        "query": "Is it safe to put metal in the microwave?",
    },
    {
        "appliance": "unknown",
        "history": history,
        "query": "I love you",
    },
    {
        "appliance": "microwave oven",
        "history": history,
        "query": "How to make popcorn without burning it?",
    },
    {
        "appliance": "washing machine",
        "history": history,
        "query": "Why is my machine not spinning?",
    },
    {
        "appliance": "microwave oven",
        "history": history,
        "query": "Can I cook eggs in the microwave?",
    },
    {
        "appliance": "washing machine",
        "history": history,
        "query": "What's the best mode to wash blood?",
    },
    {
        "appliance": "microwave oven",
        "history": history,
        "query": "How often should I clean the interior?",
    },
    {
        "appliance": "microwave oven",
        "history": history,
        "query": "Can I heat up my coffee in a paper cup?",
    },
    {
        "appliance": "washing machine",
        "history": history,
        "query": "What's the difference between delicate and normal cycles?",
    },
    {
        "appliance": "microwave oven",
        "history": history,
        "query": "How do I get rid of food odors in my microwave?",
    },
    {
        "appliance": "washing machine",
        "history": history,
        "query": "Is it okay to mix colors and whites clothes for washing?",
    },
    {
        "appliance": "microwave oven",
        "history": history,
        "query": "What's the best container for reheating pasta?",
    },
    {
        "appliance": "washing machine",
        "history": history,
        "query": "How much detergent should I use for a full load?",
    },
    {
        "appliance": "microwave oven",
        "history": history,
        "query": "Is it safe to use aluminum foil in the microwave?",
    },
    {
        "appliance": "washing machine",
        "history": history,
        "query": "Why is my machine making a loud noise during the spin cycle?",
    },
    {
        "appliance": "microwave oven",
        "history": history,
        "query": "How long should I microwave a baked potato?",
    },
]


def select_appliance(question, chat_history):
    """Select the appropriate appliance based on the user's question and chat history."""
    prompt = appliance_selection_prompt.format(
        question=question, chat_history=chat_history, appliances=appliances
    )
    response = ollama.generate(
        model=model, prompt=prompt, options={"temperature": config.TEMPERATURE}
    )
    return response["response"].strip().lower()


if __name__ == "__main__":
    chat_history = to_chat_history(history)
    ttl = len(tests)
    matched = 0
    for test in tests:
        target = test["appliance"]
        query_text = test["query"]
        result = select_appliance(query_text, chat_history=chat_history)
        if target == result:
            matched += 1
        else:
            print(f"Expected:{target}, Result:{result}, Query:{query_text}")
    print(f"{matched}/{ttl} matched")
