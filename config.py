from dotenv import load_dotenv
import os

# Load the environment variables from .env file
load_dotenv()
Config = {
    'model': os.getenv('MODEL'),
    'qa_db': os.getenv('QA_DB'),
    'dev_qa_db': os.getenv('DEV_QA_DB'),
    'pdf_file': os.getenv('PDF_FILE'),
}