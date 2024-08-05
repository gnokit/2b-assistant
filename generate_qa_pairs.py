import pypdf
import ollama
import json
import sqlite3
from config import config
from utils import extract_json_blocks, remove_trailing_commas

# Load configuration from the config.py file
model = config.MODEL
qa_db = config.QA_DB

# Prompt template for generating QA pairs from PDF pages
qa_pair_template = """
You are a professional Customer Service staff member.
Your task is to convert technical manual content into clear, concise 30 question-answer pairs.
The goal is to create a document that can be used effectively to respond to customer questions about the {manual} appliance.
This content will be used to retrieve and generate relevant information based on user queries.

**Instructions:**
1. **Content Understanding:** Read and understand the provided page of the manual.
2. **Conversion:** Create question-answer pairs based on the content. Each pair should consist of a potential customer question and its corresponding answer.
3. **Clarity and Value:** Ensure each question is relevant to customers and each answer is informative, valuable, and maintains technical accuracy.
4. **Formatting:** Present the question-answer pairs in JSON format only without code block delimiter, prefix, comments, explanation, follow-up.
5. **Customer Focus:** Prioritize information that addresses common customer queries and concerns, specifically focusing on the {manual} appliance.
6. **Double Quotes:** Ensure that all double quotes within the strings are properly escaped with a backslash (\).

**Example Ouput:**
[
  {{
    "question": "How do I turn on my device?",
    "answer": "To turn on the device, press and hold the power button located on the top right corner for 3 seconds until the screen lights up."
  }},
  {{
    "question": "What is the battery life of my product?",
    "answer": "The battery life of this product is approximately 8 hours with normal usage. This can vary depending on the settings and applications used."
  }},
  {{
    "question": "How do I connect my device to Wi-Fi?",
    "answer": "To connect to Wi-Fi, go to Settings > Network > Wi-Fi, turn on Wi-Fi, select your network from the list, and enter the password when prompted."
  }}
  ...
]


Manual Content:
```
{page_content}
```

question-answer pairs:
"""

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
                manual TEXT NOT NULL,
                PRIMARY KEY(qa_id AUTOINCREMENT))
            """
        )
        print("Table 'QA_pairs' has been created successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred while creating table: {e}")

    conn.close()


def generate_qa_pairs(page_content, manual):
    """Generate a JSON array with question-answer pairs from the given page content."""
    prompt = qa_pair_template.format(page_content=page_content, manual=manual)
    response = ollama.generate(
        model=model, prompt=prompt, options={"temperature": config.TEMPERATURE}
    )
    return response["response"]


def read_pdf(pages, pdf):
    """Read the specified pages from a PDF file and yield each page number along with its content."""
    with open(pdf, "rb") as fh:
        pdf_reader = pypdf.PdfReader(fh)
        for page_num in pages:
            pdf_page = pdf_reader.get_page(page_num)
            yield page_num, pdf_page.extract_text().strip()


def insert_qa_pair(cursor, page_num, qa_pair, manual):
    """Insert a question-answer pair into the database."""
    cursor.execute(
        "INSERT INTO qa_pairs (page_num, question, answer, manual) VALUES (?, ?, ?, ?)",
        (page_num, qa_pair["question"], qa_pair["answer"], manual),
    )


def import_qa_pairs(pages, manual, file):
    """Import question-answer pairs from the specified pages of a PDF file into a SQLite database."""
    conn = sqlite3.connect(qa_db)
    cursor = conn.cursor()
    total_qa_pairs = 0
    failed_pages = []
    for page_num, page_content in read_pdf(pages, file):
        try:
            content = generate_qa_pairs(page_content, manual)
            content = extract_json_blocks(content)
            content = remove_trailing_commas(content)
            qa_pairs = json.loads(content)
            total_qa_pairs += len(qa_pairs)
            for qa_pair in qa_pairs:
                insert_qa_pair(cursor, page_num, qa_pair, manual)
            conn.commit()
            print(
                f"page: {page_num}, number of qa: {len(qa_pairs)}, total qa: {total_qa_pairs}"
            )
        except Exception as e:
            print(f"page: {page_num}, error: {str(e)}, content:\n{content}")
            failed_pages.append(page_num)
    conn.close()
    return failed_pages


if __name__ == "__main__":
    create_qa_table()
    # import_qa_pairs(
    #     [i for i in range(30)],
    #     manual="microwave oven",
    #     file="data/OI-NN-ST25JB_MPQ_ST25JW_YPQ_HPE_180628.pdf",
    # )
    # import_qa_pairs(
    #     [33, 39],  # [i for i in range(44)],
    #     manual="washing machine",
    #     file="data/MFL70203955-EN.pdf",
    # )

    # pages = [i for i in range(1, 30)]
    # while len(pages) > 0:
    #     pages = import_qa_pairs(
    #         pages,
    #         manual="microwave oven",
    #         file="data/OI-NN-ST25JB_MPQ_ST25JW_YPQ_HPE_180628.pdf",
    #     )

    #pages = [i for i in range(1, 17)]
    pages = [10]
    while len(pages) > 0:
        pages = import_qa_pairs(
            pages,
            manual="coffee maker",
            file="data/eng_delonghi_manu_ec685.pdf",
        )
