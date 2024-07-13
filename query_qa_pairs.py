from config import chroma_client, Config

collection = chroma_client.get_collection(name=Config['collection'])

def query(query_text, thershold=1.15, n_results=5):
    result = collection.query(query_texts=[query_text], n_results=n_results)
    documents = []
    for id, distance, document in zip(result['ids'][0], result['distances'][0], result['documents'][0]):
        if distance < thershold:  # filter out results that are too similar to the query
            documents.append((id, distance, document))            
    return documents

if __name__ == "__main__":
    query_text = input("Enter your question: ")
    documnents = query(query_text)
    print(f'total documents: {len(documnents)}')
    print(documnents)