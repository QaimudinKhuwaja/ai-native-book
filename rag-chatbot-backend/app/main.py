from fastapi import FastAPI
from app.api import chat

app = FastAPI()

app.include_router(chat.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"Hello": "World from RAG Chatbot Backend!"}