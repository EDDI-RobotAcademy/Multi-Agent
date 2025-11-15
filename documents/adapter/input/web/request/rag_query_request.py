from pydantic import BaseModel

class RAGQueryRequest(BaseModel):
    query: str
    top_k: int = 5
