# Microwave Witch 🧙‍♀️

The Microwave Witch is a conversational AI assistant developed using Ollama and a Vector DB (ChromaDB) to answer questions about microwave oven operation. The project aims to create a Retrieval Augmented Generation (RAG) application using the provided microwave oven instruction manual as the source of information.

## Project Objectives

1. Convert the microwave oven operation manual content into a question-answer (QA) format and store it in a SQLite3 database (see `generate_qa_pairs.py`).
2. Process the QA records in the SQLite3 database to eliminate any useless or irrelevant information.
3. Ingest the curated QA pairs into a Vector DB (ChromaDB) to enable efficient retrieval and generation (see `ingest_qa_pairs.py`).
4. Develop a Streamlit-based user interface (UI) that allows users to interact with the Microwave Witch chatbot (see `chat.py`).

## Features

- Provides guidance on microwave usage, including cooking times, power levels, and techniques
- Offers troubleshooting tips for common microwave issues
- Suggests recipes and cooking methods for various food items
- Answers questions about microwave features and functionality

## Getting Started

1. Ensure you have Python 3.x installed on your system.
2. Clone the repository and navigate to the project directory.
3. Create a virtual environment using `venv` or your preferred tool, e.g., `python -m venv env`.
4. Activate the virtual environment:
   - On Windows: `env\Scripts\activate`
   - On macOS/Linux: `source env/bin/activate`
5. Install the required dependencies by running `pip install -r requirements.txt`.
6. Rename the `env_example` file to `.env` and modify its contents according to your needs.
7. Generate the QA pairs from the microwave oven manual by running `python generate_qa_pairs.py`.
8. Ingest the QA pairs into the ChromaDB Vector DB by running `python ingest_qa_pairs.py`.
9. Start the Streamlit-based Microwave Witch chatbot UI by running `streamlit run chat.py`.
10. Interact with the Microwave Witch chatbot and ask your microwave-related questions.

## Contributing

If you'd like to contribute to the development of the Microwave Witch, please feel free to clone the repository directly.

## Contact

For any questions or feedback about the Microwave Witch, you can reach me at:

- Email: gnokit@gmail.com

Thank you for using the Microwave Witch! I'm always here to help with your microwave-related needs.