from config import chroma_client, Config
import sqlite3

def ingest():
    """Ingest data into ChromaDB"""
    
    # Get or create a collection in ChromaDB with the name specified in the Config object.
    collection = chroma_client.get_or_create_collection(name=Config['collection'])    
    conn = sqlite3.connect(Config['dev_qa_db'])
    cursor = conn.cursor()
    # Execute a SELECT statement to retrieve data from the QA_Pairs table
    cursor.execute("SELECT qa_id, page_num, question, answer FROM qa_pairs ORDER BY page_num ASC")

    # Fetch all the rows from the result set
    rows = cursor.fetchall()

    # Add the retrieved data to ChromaDB using the add method of the collection object
    for row in rows:
        qa_id, page_num, question, answer = row
        ids=[f'qa_id_{qa_id}']
        documents=[f'{question}\n{answer}']
        metadatas=[{'page_num': page_num, 'qa_id': qa_id}]
        collection.add(ids=ids, documents=documents, metadatas=metadatas)
    
    conn.close()
    print("Ingestion complete")
    
if __name__=='__main__':
    ingest()