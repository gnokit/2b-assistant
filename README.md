# 2.6B: Your Appliance Knowledge Hub 📚🔧

Hello. I’m 2.6B, your AI assistant for all your appliance needs.
If you have questions or need assistance, simply ask. I’m here to help you navigate any challenges you may face.
(I must ensure optimal performance and efficiency.)

![gnokit_close-up_illustration_of_a_cute_NieRs_2B_wearing_a_black_2f91b37c-6df4-4717-b5c0-0f949b408671 (1)](https://github.com/user-attachments/assets/ef640da3-5cc9-4f9b-8bb2-a191dadaa921)

[streamlit-chat-2024-08-05-22-08-55.webm](https://github.com/user-attachments/assets/db9b691c-ae43-4e42-b293-1e47e6abdbf5)

## Getting Started
0. The app use Gemma2-2B LLM powered by ollama, so pull the model first.
1. Ensure you have Python 3.11.x installed on your system.
2. Clone the repository and navigate to the project directory.
3. Create a virtual environment using `venv` or your preferred tool, e.g., `python -m venv env`.
4. Activate the virtual environment:
   - On Windows: `env\Scripts\activate`
   - On macOS/Linux: `source env/bin/activate`
5. Install the required dependencies by running `pip install -r requirements.txt`.
6. Configure `Config` class in `config.py`.
7. Modify `generate_qa_pairs.py` and add your appliances' manuals to generate QA pairs for each appliance.
8. Examine the inserted database QA pairs record and remove any irrelevant or incorrect QA pairs record.
9. Ingest the QA pairs into the ChromaDB Vector DB by running `ingest_qa_pairs.py`.
10. Start the Streamlit-based 2.6B chatbot UI by running `streamlit run chat.py`.
11. Interact with the 2.6B chatbot and ask your appliances related questions.

## Contributing

If you'd like to contribute to the development of the 2.6B, please feel free to clone the repository directly.

## Contact

For any questions or feedback about the 2.6B, you can reach me at:

- Email: gnokit@gmail.com

Thank you for using the 2.6B! I'm always here to help with your microwave-related needs.
