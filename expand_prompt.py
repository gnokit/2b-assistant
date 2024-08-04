import ollama
import logging
from sentence_transformers import SentenceTransformer, util
from config import config, create_logger
import numpy as np
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
    response = ollama.generate(model, prompt)
    return response["response"].strip()


tests = [
    {
        "messages": [
            {"role": "assistant", "content": config.WELCOME_MESSAGE},
            {"content": "How do I use the washing machine?", "role": "user"},
            {
                "content": "To use a washing machine, follow these steps:\n\n1. **Sort your laundry**: Separate clothes by color, fabric type, and level of dirtiness.\n2. **Load the machine**: Place your sorted clothes into the washing machine drum.\n3. **Add detergent**: Measure the appropriate amount of detergent and add it to the detergent drawer or directly into the drum.\n4. **Select the wash cycle**: Choose the appropriate wash cycle based on the type of clothes you are washing.\n5. **Start the machine**: Close the door and press the start button to begin the wash cycle.\n\nThese are the basic steps to using a washing machine. Make sure to check the user manual for specific instructions related to your model.",
                "role": "assistant",
            },
            {
                "content": "detergent?",
                "role": "user",
            },
        ],
        "expanded": "How much detergent should I use in the washing machine?",
    },
    {
        "messages": [
            {"role": "assistant", "content": config.WELCOME_MESSAGE},
            {"content": "What is the eco mode on a washing machine?", "role": "user"},
            {
                "content": "Eco mode on a washing machine is a setting designed to save energy and water. It typically uses lower wash temperatures and longer wash times to achieve the same level of cleanliness as a standard wash cycle. This mode is ideal for lightly soiled clothes and helps reduce your environmental footprint.",
                "role": "assistant",
            },
            {
                "content": "save energy?",
                "role": "user",
            },
        ],
        "expanded": "How does the eco mode on a washing machine save energy?",
    },
    {
        "messages": [
            {"role": "assistant", "content": config.WELCOME_MESSAGE},
            {"content": "Why is my washing machine not draining?", "role": "user"},
            {
                "content": "If your washing machine is not draining, it could be due to a clogged drain hose, a faulty pump, or an issue with the machine's filter. Check these components for blockages or damage and clean or replace them as necessary. If the problem persists, it may be best to contact a professional for assistance.",
                "role": "assistant",
            },
            {
                "content": "clogged drain hose?",
                "role": "user",
            },
        ],
        "expanded": "How to fix a clogged drain hose in a washing machine?",
    },
    {
        "messages": [
            {"role": "assistant", "content": config.WELCOME_MESSAGE},
            {
                "content": "What is the delicate cycle on a washing machine?",
                "role": "user",
            },
            {
                "content": "The delicate cycle on a washing machine is designed for washing delicate fabrics such as silk, lace, and other lightweight materials. This cycle typically uses a gentler wash action, lower spin speeds, and cooler water temperatures to prevent damage to delicate items.",
                "role": "assistant",
            },
            {
                "content": "gentle wash?",
                "role": "user",
            },
        ],
        "expanded": "How to use the delicate cycle on a washing machine for a gentle wash?",
    },
    {
        "messages": [
            {"role": "assistant", "content": config.WELCOME_MESSAGE},
            {"content": "How do I remove tough stains from clothes?", "role": "user"},
            {
                "content": "To remove tough stains from clothes, follow these steps:\n\n1. **Pre-treat the stain**: Apply a stain remover or a small amount of detergent directly to the stain and let it sit for a few minutes.\n2. **Gently rub the stain**: Use a soft brush or your fingers to gently rub the stain remover into the fabric.\n3. **Wash the item**: Place the stained item in the washing machine and wash it on the appropriate cycle for the fabric type.\n4. **Check the stain**: After washing, check to see if the stain is gone. If not, repeat the process before drying the item.",
                "role": "assistant",
            },
            {
                "content": "pre-treat?",
                "role": "user",
            },
        ],
        "expanded": "How to pre-treat tough stains before using the washing machine?",
    },
    {
        "messages": [
            {"role": "assistant", "content": config.WELCOME_MESSAGE},
            {"content": "How do I use a microwave oven?", "role": "user"},
            {
                "content": "To use a microwave oven, follow these steps:\n\n1. **Place food in a microwave-safe container**: Ensure the container is suitable for microwave use.\n2. **Cover the food**: Use a microwave-safe lid or microwave-safe plastic wrap to cover the food.\n3. **Set the cooking time and power level**: Enter the desired cooking time and adjust the power level if necessary.\n4. **Start the microwave**: Press the start button to begin cooking.\n5. **Check and stir the food**: Pause the microwave halfway through cooking to check and stir the food for even heating.",
                "role": "assistant",
            },
            {
                "content": "microwave-safe container?",
                "role": "user",
            },
        ],
        "expanded": "What types of containers are microwave-safe?",
    },
    {
        "messages": [
            {"role": "assistant", "content": config.WELCOME_MESSAGE},
            {"content": "How do I defrost chicken in the microwave?", "role": "user"},
            {
                "content": "To defrost chicken in the microwave, follow these steps:\n\n1. **Remove packaging**: Take the chicken out of any packaging or plastic wrap.\n2. **Place in a microwave-safe dish**: Put the chicken in a microwave-safe dish to catch any drips.\n3. **Set the microwave to defrost mode**: Use the defrost setting on your microwave and enter the weight of the chicken.\n4. **Check and rotate**: Pause the microwave halfway through defrosting to check and rotate the chicken for even defrosting.\n5. **Cook immediately**: Once defrosted, cook the chicken immediately to ensure food safety.",
                "role": "assistant",
            },
            {
                "content": "defrost setting?",
                "role": "user",
            },
        ],
        "expanded": "How to use the defrost setting on a microwave oven for chicken?",
    },
    {
        "messages": [
            {"role": "assistant", "content": config.WELCOME_MESSAGE},
            {"content": "Can I cook eggs in the microwave?", "role": "user"},
            {
                "content": "Yes, you can cook eggs in the microwave. Here are a few methods:\n\n1. **Scrambled eggs**: Beat eggs in a microwave-safe bowl, add a splash of milk, and microwave in short intervals, stirring in between.\n2. **Poached eggs**: Crack an egg into a microwave-safe cup, add a bit of water, cover with a microwave-safe plate, and microwave for about a minute.\n3. **Hard-boiled eggs**: Place eggs in a microwave-safe bowl, cover with water, and microwave in short intervals, checking frequently to avoid explosions.",
                "role": "assistant",
            },
            {
                "content": "scrambled eggs?",
                "role": "user",
            },
        ],
        "expanded": "How to cook scrambled eggs in a microwave oven?",
    },
    {
        "messages": [
            {"role": "assistant", "content": config.WELCOME_MESSAGE},
            {"content": "How do I clean my microwave oven?", "role": "user"},
            {
                "content": "To clean your microwave oven, follow these steps:\n\n1. **Remove loose debris**: Take out any loose crumbs or food particles.\n2. **Steam clean**: Fill a microwave-safe bowl with water and a few slices of lemon, then microwave on high for a few minutes to create steam.\n3. **Wipe down**: Use a damp cloth or sponge to wipe down the interior, including the walls, ceiling, and turntable.\n4. **Clean the exterior**: Wipe down the exterior with a damp cloth and mild detergent if needed.",
                "role": "assistant",
            },
            {
                "content": "steam clean?",
                "role": "user",
            },
        ],
        "expanded": "How to steam clean a microwave oven?",
    },
    {
        "messages": [
            {"role": "assistant", "content": config.WELCOME_MESSAGE},
            {"content": "How long should I microwave a baked potato?", "role": "user"},
            {
                "content": "To microwave a baked potato, follow these steps:\n\n1. **Wash the potato**: Scrub the potato clean and pat it dry.\n2. **Pierce the potato**: Use a fork to poke holes all over the potato to allow steam to escape.\n3. **Microwave on high**: Place the potato on a microwave-safe plate and microwave on high for about 5-7 minutes, turning halfway through.\n4. **Check for doneness**: The potato is done when it is soft and can be easily pierced with a fork. If not done, continue microwaving in 1-minute intervals.",
                "role": "assistant",
            },
            {
                "content": "pierce the potato?",
                "role": "user",
            },
        ],
        "expanded": "Why should I pierce a potato before microwaving it?",
    },
]



if __name__ == "__main__":
    logger.setLevel(logging.DEBUG)    
    st = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    distances = []
    for test in tests:
        messages = test["messages"]
        query = test["messages"][-1]["content"]
        expanded = test["expanded"]
        result = expand_prompt(chat_history=messages)
        embedding_1= st.encode(expanded, convert_to_tensor=True)
        embedding_2 = st.encode(result, convert_to_tensor=True)
        distance = util.pytorch_cos_sim(embedding_1, embedding_2)[0][0]
        distances.append(distance)
        print(f"Query:{query}\nExpected:{expanded}\nResult:{result}\nDistance:{distance}")
    print(f"Average Result: {np.array(distances).mean()}")
