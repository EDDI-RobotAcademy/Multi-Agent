from typing import List, Optional

from anonymous_board.application.port.anonymous_board_repository_port import AnonymousBoardRepositoryPort
from anonymous_board.domain.anonymous_board import AnonymousBoard


class AnonymousBoardUseCase:
    def __init__(self, board_repo: AnonymousBoardRepositoryPort):
        self.board_repo = board_repo

    def create_board(self, title: str, content: str) -> AnonymousBoard:
        board = AnonymousBoard(title=title, content=content)
        return self.board_repo.save(board)

    def get_board(self, board_id: int) -> Optional[AnonymousBoard]:
        return self.board_repo.get_by_id(board_id)

    def list_boards(self) -> List[AnonymousBoard]:
        return self.board_repo.list_all()

    def delete_board(self, board_id: int) -> None:
        self.board_repo.delete(board_id)
