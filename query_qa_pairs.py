from config import chroma_client, Config, create_logger
import logging

logger = create_logger("query_qa_pairs")  # Create a logger for this module

# Connect to the Chroma database and get the collection
collection = chroma_client.get_collection(name=Config["collection"])

top_k = Config['top_k']
max_distance = Config['max_distance']

def query(query_text):
    """Perform similary search of query_text and return the top_k documents"""
    result = collection.query(query_texts=[query_text], n_results=top_k)
    documents = []
    for id, distance, document in zip(
        result["ids"][0], result["distances"][0], result["documents"][0]
    ):
        logger.debug("id: {}, distance: {}, document: {}".format(id, distance, document[:20]))
        # filter out results with distance greater than max_distance
        if distance < max_distance: 
            documents.append((id, distance, document))
    
    return documents


def query_to_context(query_text):
    """Perform similary search of query_text and convert to QA pairs of Q and A"""
    documents = query(query_text=query_text)
    context = ""
    for _, _, document in documents:
        pairs = document.split("\n")
        q = pairs[0]
        a = "\n".join(pairs[1:])
        context += f"Q: {q}\nA: {a}\n\n"
    return context


if __name__ == "__main__":
    logger.setLevel(logging.DEBUG)
    query_text = input("Enter your question: ")
    context = query_to_context(query_text)
    print(context)
