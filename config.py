from dotenv import load_dotenv
import os
import chromadb
import logging
from chromadb.config import Settings

# Load the environment variables from .env file
load_dotenv(override=True)

# initial configuration for application
Config = {
    "model": os.getenv("MODEL"),
    "qa_db": os.getenv("QA_DB"),    
    "pdf_file": os.getenv("PDF_FILE"),
    "collection": os.getenv("COLLECTION"),
    "top_k": int(os.getenv("TOP_K")),
    "max_distance": float(os.getenv("MAX_DISTANCE")),
}

# initialize ChromaDB client for persistent storage of data. This is a local database
chroma_client = chromadb.PersistentClient(
    settings=Settings(anonymized_telemetry=False, allow_reset=True)
)

def create_logger(name):    
    # Create a logger instance
    logger = logging.getLogger(name)
    # Create a console handler and set its stream to sys.stdout (which is the default)
    handler = logging.StreamHandler()
    # Create a formatter and specify the format of the log messages
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # Set the formatter for the console handler
    handler.setFormatter(formatter)
    # Add the console handler to the logger
    logger.addHandler(handler)
    return logger