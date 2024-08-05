import chromadb
import logging
from chromadb.config import Settings


class Config:
    def __init__(self):
        # Local ollama model to execute all llm request
        self.MODEL: str = "gemma2:2b-instruct-q8_0"
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
        # The temperature of the model
        self.TEMPERATURE: float = 0.0
        # Installed appliances list
        self.APPLICANTS: list = ["washing machine", "microwave oven"]
        self.WELCOME_MESSAGE = """Hello. I’m 2.6B, your AI assistant for all your appliance needs.
If you have questions or need assistance, simply ask. I’m here to help you navigate any challenges you may face.
(I must ensure optimal performance and efficiency.)"""


config = Config()

# initialize ChromaDB client for persistent storage of data. This is a local database
chroma_client = chromadb.PersistentClient(
    settings=Settings(anonymized_telemetry=False, allow_reset=True)
)


def create_logger(name):
    """This function creates and configures a logger with console logging."""
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
