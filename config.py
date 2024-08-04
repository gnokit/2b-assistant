import chromadb
import logging
from chromadb.config import Settings


class Config:
    def __init__(self):
        # Local ollama model to execute all llm request
        self.MODEL: str = "gemma2:2b"
        # Local ollama model for moderation.
        self.GUARD_MODEL: str = "rongfengliang/shieldgemma:2b"
        # Chromadb to store ALL documents
        self.QA_COLL: str = "qa_pairs"
        # Location of your QA database (sqlite3) for QA records and other records
        self.QA_DB: str = "data/2b_assistant.db"
        # Top K documents will be retrieved
        self.TOP_K: int = 5
        # Max. distance of documents wil be filtered out
        self.MAX_DIST: float = 1.0
        # Installed appliances list
        self.APPLICANTS: list = ["washing machine", "microwave oven"]
        self.WELCOME_MESSAGE = """Hi there! 😊 I'm Elara, your go-to AI assistant for all things household appliances.
🏠✨ Got a question or need help troubleshooting? Just ask, and I'll do my best to assist you! What can I help you with today?"""


config = Config()

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
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    # Set the formatter for the console handler
    handler.setFormatter(formatter)
    # Add the console handler to the logger
    logger.addHandler(handler)
    return logger
