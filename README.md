# RAG-Chatbot

This project is a FastAPI-based chatbot that uses OpenAI's GPT models to answer questions based on the content of PDF files. The chatbot creates vector databases from the PDFs and uses these databases to provide context-aware responses.

## Features

- **Update Vector Databases:** Automatically processes all PDFs in the root directory and creates vector databases for each PDF.
- **Ask Questions:** Allows users to ask questions based on the content of a specific PDF.

## Requirements

- Python 3.7+
- openai
- pypdf
- faiss-cpu
- langchain
- langchain-community
- langchain_openai
- fastapi
- uvicorn
- python-dotenv

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/rag-chatbot.git
   cd rag-chatbot
   ```
2. **Create and activate a virtual environment:**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. **Install the dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Create a .env file in the root directory and add your OpenAI API key:**
   OPENAI_API_KEY=your_openai_api_key

## Usage

1. **Run the FastAPI server:**
   ```sh
   uvicorn server:app --host "localhost" --port 3050
   ```
2. **Update Vector Databases:**
   This endpoint processes all PDFs in the root directory and creates vector databases for each PDF.
   ```sh
   curl -X POST "http://localhost:3050/update_vectordb"
   ```
3. **Ask Questions for a Specific PDF:**
   This endpoint handles questions for a specific PDF
   ```sh
   curl -X POST "http://localhost:3050/ask_questions/{pdf_name}" -H "Content-Type: application/json" -d '{
        "conversation": [
            {
                "role": "user",
                "content": "Hi, how are you doing?"
            }
        ]
   }'
   ```

## Contributing

 1. Fork the repository.
 2. Create a new branch:
    ```sh
    git checkout -b feature-branch
    ```
 3. Make your changes.
 4. Commit your changes:
    ```sh
    git commit -m 'Add some feature'
    ```
 5. Push to the branch:
    ```sh
    git push origin feature-branch
    ```
 6. Open a pull request.

 ## License

 This project is licensed under the MIT License.