from abc import ABC, abstractmethod
from typing import List, Optional

from anonymous_board.domain.anonymous_board import AnonymousBoard


class AnonymousBoardRepositoryPort(ABC):

    @abstractmethod
    def save(self, board: AnonymousBoard) -> AnonymousBoard:
        pass

    @abstractmethod
    def get_by_id(self, board_id: int) -> Optional[AnonymousBoard]:
        pass

    @abstractmethod
    def list_all(self) -> List[AnonymousBoard]:
        pass

    @abstractmethod
    def delete(self, board_id: int) -> None:
        pass
