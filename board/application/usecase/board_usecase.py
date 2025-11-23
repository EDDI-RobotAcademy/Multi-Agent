from typing import List, Tuple

from board.application.port.board_repository_port import BoardRepositoryPort
from board.domain.board import Board


class BoardUsecase:
    def __init__(self, repository: BoardRepositoryPort):
        self.repository = repository

    def create_board(self, title: str, content: str, author_id: int) -> Board:
        board = Board.create(title, content, author_id)
        return self.repository.save(board)

    def get_board(self, board_id: int) -> Board:
        board = self.repository.find_by_id(board_id)
        if not board:
            raise ValueError("Board not found")
        return board

    def get_boards_by_author(self, author_id: str) -> List[Board]:
        return self.repository.find_by_author(author_id)

    def get_all_boards(self, page: int = 1, size: int = 10) -> Tuple[List[Board], int]:
        boards, total = self.repository.find_all(page=page, size=size)
        return boards, total

    def delete_board(self, board_id: int):
        self.repository.delete(board_id)

    def update_board(self, board_id: int, title: str, content: str) -> Board:
        board = self.repository.find_by_id(board_id)
        if not board:
            raise ValueError("Board not found")

        board.update(title, content)
        return self.repository.save(board)
