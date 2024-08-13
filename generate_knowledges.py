import pypdf
import ollama
import json
import sqlite3
from config import config
from utils import extract_json_blocks, remove_trailing_commas

# Load configuration from the config.py file
model = config.MODEL
qa_db = config.KNOWLEDGE_DB

knowledge_template = """
You are a professional Customer Service staff member.
Your task is to extract 30 key knowledges from an appliance operation manual.
Your goal is to create a concise list of knowledges that can be used to provide relevant information to users based on their queries.

**Instructions:**
1. **Content Understanding:** Read and understand the provided page of the manual.
2. **Fact Extraction:** Identify the most important and relevant knowledges from the content.
3. **Clarity and Conciseness:** Express each fact clearly and concisely, avoiding unnecessary details.
4. **Inclusion of Appliance Name:** Each fact should explicitly mention the name of the {appliance} to provide context.
5. **Formatting:** Present the knowledges in a bulleted list format, with each fact starting with a dash (-).
6. **Accuracy:** Ensure that all knowledges are technically accurate and align with the information provided in the manual.
7. **Relevance:** Focus on knowledges that are likely to be useful for users when operating or troubleshooting the {appliance}.
8. **Output Format:** Return the list of knowledges without any comments, explanation, or prefix.

**Example Output:**
- The {appliance} has a power button located on the top right corner.
- Pressing and holding the power button for 3 seconds turns on the {appliance}.
- The {appliance} has a battery life of approximately 8 hours with normal usage.
- Battery life for the {appliance} may vary depending on the settings and applications used.
- To connect the {appliance} to Wi-Fi, go to Settings > Network > Wi-Fi and turn on Wi-Fi.
- Select your network from the list and enter the password when prompted.

Manual Content:
```
{page_content}
```

Facts:
"""


def create_knowledges_table():
    conn = sqlite3.connect(qa_db)
    c = conn.cursor()

    try:
        c.execute(
            """
			CREATE TABLE IF NOT EXISTS knowledges (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				appliance TEXT,
				page_num NUMBER,
				knowledge TEXT NOT NULL,
				created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
			);
			"""
        )
        print("Table 'knowledges' has been created successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred while creating table: {e}")

    conn.close()


def generate_knowledges(page_content, appliance):
    """Generate knowledges from the given page content."""
    prompt = knowledge_template.format(page_content=page_content, appliance=appliance)
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


def insert_knowledge(cursor, page_num, knowledge, appliance):
    """Insert a knowledge into the database."""
    cursor.execute(
        "INSERT INTO knowledges (page_num, knowledge, appliance) VALUES (?, ?, ?)",
        (page_num, knowledge, appliance),
    )


def import_knowledges(pages, appliance, file):
    """Import knowledges from the specified pages of a PDF file into a SQLite database."""
    conn = sqlite3.connect(qa_db)
    cursor = conn.cursor()
    total_knowledges = 0
    failed_pages = []
    for page_num, page_content in read_pdf(pages, file):
        try:
            content = generate_knowledges(page_content, appliance)       
			page_knowledges = 0
            for knowledge in content.split("\n"):
				if knowledge.startswith("-"):
					insert_fact(cursor, page_num, knowledge[1:].strip(), appliance)					
					conn.commit()
					page_knowledges += 1
			total_knowledges += page_knowledges
            print(
                f"page: {page_num}, number of knowledge: {page_knowledges}, total qa: {total_knowledges}"
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
        pages = import_knowledges(
            pages,
            manual="coffee maker",
            file="data/eng_delonghi_manu_ec685.pdf",
        )
