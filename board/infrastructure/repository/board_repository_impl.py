from typing import List, Tuple

from board.application.port.board_repository_port import BoardRepositoryPort
from board.domain.board import Board
from board.infrastructure.orm.board_orm import BoardORM
from config.database.session import SessionLocal

class BoardRepositoryImpl(BoardRepositoryPort):
    def __init__(self):
        self.db = SessionLocal()

    def save(self, board: Board) -> Board:
        if board.id is None:
            # 새 게시글 생성
            orm = BoardORM(
                title=board.title,
                content=board.content,
                author_id=board.author_id
            )
            self.db.add(orm)
            self.db.commit()
            self.db.refresh(orm)
            board.id = orm.id
            board.created_at = orm.created_at
            board.updated_at = orm.updated_at
        else:
            # 기존 게시글 업데이트
            orm = self.db.get(BoardORM, board.id)
            if orm is None:
                raise ValueError("Board not found for update")

            orm.title = board.title
            orm.content = board.content
            self.db.commit()
            self.db.refresh(orm)
            board.updated_at = orm.updated_at

        return board

    def find_by_id(self, board_id: int) -> Board | None:
        orm = self.db.get(BoardORM, board_id)
        if orm is None:
            return None
        board = Board(
            title=orm.title,
            content=orm.content,
            author_id=orm.author_id
        )
        board.id = orm.id
        board.created_at = orm.created_at
        board.updated_at = orm.updated_at
        return board

    def find_by_author(self, author_id: str):
        orms = self.db.query(BoardORM).filter(BoardORM.author_id == author_id).all()
        return [Board(title=o.title, content=o.content, author_id=o.author_id) for o in orms]

    def find_all(self, page: int, size: int) -> tuple[list[Board], int]:
        query = self.db.query(BoardORM)

        total = query.count()  # 전체 게시물 수

        orms = query.offset((page - 1) * size).limit(size).all()

        boards = []
        for o in orms:
            b = Board(o.title, o.content, o.author_id)
            b.id = o.id
            b.created_at = o.created_at
            b.updated_at = o.updated_at
            boards.append(b)

        return boards, total

    def delete(self, board_id: int):
        orm = self.db.get(BoardORM, board_id)
        if orm:
            self.db.delete(orm)
            self.db.commit()
