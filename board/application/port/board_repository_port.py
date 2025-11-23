from abc import ABC, abstractmethod
from typing import Optional, List, Tuple

from board.domain.board import Board


class BoardRepositoryPort(ABC):
    @abstractmethod
    def save(self, board: Board) -> Board:
        pass

    @abstractmethod
    def find_by_id(self, board_id: int) -> Optional[Board]:
        pass

    @abstractmethod
    def find_by_author(self, author_id: str) -> List[Board]:
        pass

    @abstractmethod
    def find_all(self, page: int, size: int) -> list[Board]:
        pass

    @abstractmethod
    def delete(self, board_id: int) -> None:
        pass
