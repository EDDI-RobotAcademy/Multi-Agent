from typing import Optional
from datetime import datetime

class AnonymousBoard:
    def __init__(self, title: str, content: str):
        self.id: Optional[int] = None
        self.title = title
        self.content = content
        self.created_at: datetime = datetime.utcnow()
        self.updated_at: datetime = datetime.utcnow()

    def update(self, title: str, content: str):
        self.title = title
        self.content = content
        self.updated_at = datetime.utcnow()
