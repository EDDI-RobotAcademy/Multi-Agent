from pydantic import BaseModel

class SentimentRequest(BaseModel):
    text: str
