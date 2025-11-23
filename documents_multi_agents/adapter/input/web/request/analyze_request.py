from pydantic import BaseModel


class AnalyzeRequest(BaseModel):
    doc_id: int
    doc_url: str
    question: str
