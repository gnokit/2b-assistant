import pypdf
import ollama
import json
import sqlite3
from config import Config

# Load configuration from the config.py file
file = Config["pdf_file"]
model = Config["model"]
qa_db = Config["qa_db"]

# Prompt template for generating QA pairs from PDF pages
qa_pair_template = """
For the provided microwave oven instruction manual content, generate a JSON array with 20 question-answer pairs 
without any formatting, comments, explanations, or prefixes.

Page content:
{page_content}

JSON array:
"""

import sqlite3

import sqlite3


def create_qa_table():
    conn = sqlite3.connect(qa_db)
    c = conn.cursor()

    try:
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS qa_pairs (
                qa_id INTEGER, 
                page_num INTEGER, 
                question TEXT NOT NULL, 
                answer TEXT NOT NULL, 
                PRIMARY KEY(qa_id AUTOINCREMENT))
            """
        )
        print("Table 'QA_pairs' has been created successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred while creating table: {e}")

    conn.close()


def generate_qa_pairs(page_content):
    """Generate a JSON array with 20 question-answer pairs from the given page content."""
    prompt = qa_pair_template.format(page_content=page_content)
    response = ollama.generate(model=model, prompt=prompt)
    return response["response"]


def read_pdf(pages, pdf):
    """Read the specified pages from a PDF file and yield each page number along with its content."""
    with open(pdf, "rb") as fh:
        pdf_reader = pypdf.PdfReader(fh)
        for page_num in pages:
            pdf_page = pdf_reader.get_page(page_num)
            yield page_num, pdf_page.extract_text().strip()


def insert_qa_pair(cursor, page_num, qa_pair):
    """Insert a question-answer pair into the database."""
    cursor.execute(
        "INSERT INTO qa_pairs (page_num, question, answer) VALUES (?, ?, ?)",
        (page_num, qa_pair["question"], qa_pair["answer"]),
    )


def import_qa_pairs(pages):
    """Import question-answer pairs from the specified pages of a PDF file into a SQLite database."""
    conn = sqlite3.connect(qa_db)
    cursor = conn.cursor()
    total_qa_pairs = 0
    for page_num, page_content in read_pdf(pages, file):
        try:
            content = generate_qa_pairs(page_content)
            qa_pairs = json.loads(content)
            total_qa_pairs += len(qa_pairs)
            for qa_pair in qa_pairs:
                insert_qa_pair(cursor, page_num, qa_pair)
            conn.commit()
            print(
                f"page: {page_num}, number of qa: {len(qa_pairs)}, total qa: {total_qa_pairs}"
            )
        except Exception as e:
            print(f"page: {page_num}, error: {str(e)}")
    conn.close()


if __name__ == "__main__":
    create_qa_table();
    # import all english pages
    # import_qa_pairs([i for i in range(30)])
    # import failed pages only
    import_qa_pairs([13, 14, 27])
