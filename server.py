from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
import os
from openai import OpenAI
from brain import get_index_for_pdf
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")

client = OpenAI(api_key=openai_api_key)

class ConversationMessage(BaseModel):
    role: str
    content: str

class ConversationRequest(BaseModel):
    conversation: List[ConversationMessage]

@app.post("/update_vectordb")
async def update_vectordb():
    pdf_files = [f for f in os.listdir() if f.endswith('.pdf')]
    if not pdf_files:
        raise HTTPException(status_code=404, detail="No PDF files found in the root directory.")
    
    for pdf_file in pdf_files:
        with open(pdf_file, "rb") as f:
            pdf_content = f.read()
        
        vectordb = get_index_for_pdf([pdf_content], [pdf_file], openai_api_key)
        vectordb.save_local(f"vectordb-{pdf_file}")
    
    return {"message": "Vector databases updated for all PDFs in the root directory."}

@app.post("/ask_questions/{pdf_name}")
async def ask_questions(pdf_name: str, request: ConversationRequest):
    vectordb_path = f"vectordb-{pdf_name}"
    if not os.path.exists(os.path.join(vectordb_path, "index.faiss")) or not os.path.exists(os.path.join(vectordb_path, "index.pkl")):
        raise HTTPException(status_code=400, detail="Vector database not found. Please update the vector database first.")

    vectordb = FAISS.load_local(vectordb_path, OpenAIEmbeddings(openai_api_key=openai_api_key), allow_dangerous_deserialization=True)
    # extract the last message from the conversation and it should be from the user
    last_message = request.conversation[-1]
    if last_message.role != "user":
        raise HTTPException(status_code=400, detail="Last message should be from the user.")
    
    context = vectordb.similarity_search(last_message.content, k=3)
    context_text = "\n".join([doc.page_content for doc in context])

    prompt_template = """
        You are a helpful Assistant who answers to users questions based on multiple contexts given to you.

        Keep your answer short and to the point.

        The evidence are the context of the pdf extract with metadata.

        Reply "Not applicable" if text is irrelevant.

        The PDF content is:
        {pdf_extract}
    """
    prompt = prompt_template.format(pdf_extract=context_text)
    
    # Append the prompt template to the beginning of the conversation
    messages = [{"role": "system", "content": prompt}] + [msg.model_dump() for msg in request.conversation]

    response = client.chat.completions.create(model="gpt-4o-mini", messages=messages, stream=False)

    return JSONResponse(content={"response": response.choices[0].message.content})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=3050)