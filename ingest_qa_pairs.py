from config import chroma_client, config
import sqlite3

def ingest():
    """Ingest data into ChromaDB"""

    # Get or create a collection in ChromaDB with the name specified in the Config object.
    collection = chroma_client.get_or_create_collection(name=config.QA_COLL)
    conn = sqlite3.connect(config.QA_DB)
    cursor = conn.cursor()
    # Execute a SELECT statement to retrieve data from the QA_Pairs table
    cursor.execute(
        "SELECT qa_id, page_num, question, answer, manual FROM qa_pairs ORDER BY qa_id ASC"
    )

    # Fetch all the rows from the result set
    rows = cursor.fetchall()

    # Add the retrieved data to ChromaDB using the add method of the collection object
    for row in rows:
        # Unpack the row into variables for easier access
        qa_id, page_num, question, answer, manual = row
        ids = [f"qa_id_{qa_id}"]
        documents = [f"Question: {question}\nAnswer: {answer}\n"]
        metadatas = [{"page_num": page_num, "qa_id": qa_id, "manual": manual}]
        collection.add(ids=ids, documents=documents, metadatas=metadatas)

    conn.close()
    print("Ingestion complete")


if __name__ == "__main__":
    ingest()
