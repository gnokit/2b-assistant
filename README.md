# HomeWise: Your Appliance Knowledge Hub 📚🔧

Hi there! 😊 I'm Elara, your go-to AI assistant for all things household appliances.
🏠✨ Got a question or need help troubleshooting? Just ask, and I'll do my best to assist you! What can I help you with today?

## Demonstration
[demo.webm](https://github.com/user-attachments/assets/2d15966b-5269-411e-aae5-372038bf1132)

## Getting Started

1. Ensure you have Python 3.11.x installed on your system.
2. Clone the repository and navigate to the project directory.
3. Create a virtual environment using `venv` or your preferred tool, e.g., `python -m venv env`.
4. Activate the virtual environment:
   - On Windows: `env\Scripts\activate`
   - On macOS/Linux: `source env/bin/activate`
5. Install the required dependencies by running `pip install -r requirements.txt`.
6. Rename the `env_example` file to `.env` and modify its contents according to your needs.
7. Modify `generate_qa_pairs.py` and generate the QA pairs from the microwave oven manual and store into sqlite database.
8. Examine the inserted database QA pairs record and remove any irrelevant or incorrect QA pairs record.
9. Ingest the QA pairs into the ChromaDB Vector DB by running `python ingest_qa_pairs.py`.
10. Start the Streamlit-based Microwave Witch chatbot UI by running `streamlit run chat.py`.
11. Interact with the Microwave Witch chatbot and ask your microwave-related questions.

## Contributing

If you'd like to contribute to the development of the Microwave Witch, please feel free to clone the repository directly.

## Contact

For any questions or feedback about the Microwave Witch, you can reach me at:

- Email: gnokit@gmail.com

Thank you for using the Microwave Witch! I'm always here to help with your microwave-related needs.
