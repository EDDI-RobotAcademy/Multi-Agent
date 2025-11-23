from pydantic import BaseModel
from datetime import datetime
from board.domain.board import Board

class BoardResponse(BaseModel):
    id: int
    title: str
    content: str
    author_nickname: str  # id 대신 nickname
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_board(cls, board: Board, nickname: str):
        return cls(
            id=board.id,
            title=board.title,
            content=board.content,
            author_nickname=nickname,
            created_at=board.created_at,
            updated_at=board.updated_at
        )
