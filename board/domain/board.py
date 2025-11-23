from typing import Optional
from datetime import datetime

class Board:
    def __init__(self, title: str, content: str, author_id: int):
        self.id: Optional[int] = None
        self.title = title
        self.content = content
        self.author_id = author_id
        self.created_at: datetime = datetime.utcnow()
        self.updated_at: datetime = datetime.utcnow()

    @classmethod
    def create(cls, title: str, content: str, author_id: int) -> "Board":
        if not title:
            raise ValueError("Title cannot be empty")
        if not content:
            raise ValueError("Content cannot be empty")
        return cls(title, content, author_id)

    def update(self, title: str, content: str):
        self.title = title
        self.content = content
        self.updated_at = datetime.utcnow()
