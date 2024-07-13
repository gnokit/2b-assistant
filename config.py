from dotenv import load_dotenv
import os
import chromadb
from chromadb.config import Settings

# Load the environment variables from .env file
load_dotenv()
Config = {
    'model': os.getenv('MODEL'),
    'qa_db': os.getenv('QA_DB'),
    'dev_qa_db': os.getenv('DEV_QA_DB'),
    'pdf_file': os.getenv('PDF_FILE'),
    'collection': os.getenv('COLLECTION'),
}

chroma_client = chromadb.PersistentClient(    
    settings=Settings(anonymized_telemetry=False, allow_reset=True)
)