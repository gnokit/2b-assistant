from config import chroma_client, Config

# Connect to the Chroma database and get the collection
collection = chroma_client.get_collection(name=Config["collection"])

def query(query_text, thershold=1.15, n_results=5):
    """Perform similary search of query_text and return the top n_results documents"""
    result = collection.query(query_texts=[query_text], n_results=n_results)
    documents = []
    for id, distance, document in zip(
        result["ids"][0], result["distances"][0], result["documents"][0]
    ):
        # filter out results with distance greater than Thershold
        if distance < thershold: 
            documents.append((id, distance, document))
    
    return documents


def query_to_context(query_text, thershold=1.15, n_results=5):
    """Perform similary search of query_text and convert to QA pairs of Q and A"""
    documents = query(query_text=query_text, thershold=thershold, n_results=n_results)
    context = ""
    for _, _, document in documents:
        pairs = document.split("\n")
        q = pairs[0]
        a = "\n".join(pairs[1:])
        context += f"Q: {q}\nA: {a}\n\n"
    return context


if __name__ == "__main__":
    query_text = input("Enter your question: ")
    context = query_to_context(query_text)
    print(context)
