from pydantic import BaseModel
from datetime import datetime

class AnonymousBoardResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
