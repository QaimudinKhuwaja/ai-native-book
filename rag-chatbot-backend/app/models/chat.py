from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    query: str

class Source(BaseModel):
    url: str
    page_title: str
    chunk_index: int
    content: str # The content of the retrieved chunk

class ChatResponse(BaseModel):
    answer: str
    sources: List[Source]