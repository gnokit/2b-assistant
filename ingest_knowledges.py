from config import chroma_client, config
import sqlite3

def ingest():
    """Ingest data into ChromaDB"""

    # Get or create a collection in ChromaDB with the name specified in the Config object.
    collection = chroma_client.get_or_create_collection(name=config.KNOWLEDGE_COL)
    conn = sqlite3.connect(config.KNOWLEDGE_DB)
    cursor = conn.cursor()
    # Execute a SELECT statement to retrieve data from the Knowledge table
    cursor.execute(
        "SELECT id, page_num, knowledge, appliance FROM knowledges ORDER BY id ASC"
    )

    # Fetch all the rows from the result set
    rows = cursor.fetchall()

    # Add the retrieved data to ChromaDB using the add method of the collection object
    for row in rows:
        # Unpack the row into variables for easier access
        id, page_num, knowledge, appliance = row
        ids = [f"knowledge_id_{id}"]
        documents = [knowledge]
        metadatas = [{"page_num": page_num, "appliance": appliance}]
        collection.add(ids=ids, documents=documents, metadatas=metadatas)

    conn.close()
    print("Ingestion complete")


if __name__ == "__main__":
    ingest()
