from typing import List
from pydantic import BaseModel
from board.adapter.input.web.response.board_response import BoardResponse
from board.domain.board import Board

class BoardListResponse(BaseModel):
    boards: List[BoardResponse]
    total: int
    page: int
    size: int

    @classmethod
    def from_boards(cls, boards: list[Board], nicknames: dict[int, str], page: int, size: int, total: int):

        return cls(
            boards=[BoardResponse.from_board(b, nicknames.get(b.author_id, "Unknown")) for b in boards],
            total=total,
            page=page,
            size=size
        )
