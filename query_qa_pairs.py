from config import chroma_client, config, create_logger
import logging
import numpy as np

logger = create_logger("query_qa_pairs")  # Create a logger for this module

# Connect to the Chroma database and get the collection
collection = chroma_client.get_collection(name=config.QA_COLL)


def query(manual, query_text, top_k, max_distance):
    """Perform similary search of query_text and return the top_k documents"""
    result = collection.query(
        query_texts=[query_text], n_results=top_k, where={"manual": manual}
    )
    documents = []
    for id, distance, document in zip(
        result["ids"][0], result["distances"][0], result["documents"][0]
    ):
        logger.debug(
            "id: {}, distance: {}, document: {}".format(id, distance, document[:20])
        )
        # filter out results with distance greater than max_distance
        if distance < max_distance:
            documents.append((id, distance, document))

    return documents


def query_to_context(manual, query_text):
    """Perform similary search of query_text and convert to QA pairs of Q and A"""
    top_k = config.TOP_K
    max_distance = config.MAX_DIST
    documents = query(
        manual, query_text=query_text, top_k=top_k, max_distance=max_distance
    )
    context = ""
    for _, _, document in documents:
        context += f"{document}\n"
    return context


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
        "appliance": "washing machine",
        "query": "How to pre-treat tough stains before using the washing machine?",
    },
    {
        "appliance": "microwave oven",
        "query": "What types of containers are microwave-safe?",
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


if __name__ == "__main__":
    logger.setLevel(logging.INFO)
    for test in tests:
        query_text = test["query"]
        manual = test["appliance"]
        result = query(
            manual=manual, query_text=query_text, top_k=5, max_distance=1.0
        )
        total_docs = len(result)
        distances = [distance for _, distance, doc in result]
        avg_dist = np.array(distances).mean()
        print(f"Average:{avg_dist}, Total Documents:{total_docs}, Query:{query_text}")