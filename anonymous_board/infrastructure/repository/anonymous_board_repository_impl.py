from typing import List, Optional
from sqlalchemy.orm import Session

from anonymous_board.application.port.anonymous_board_repository_port import AnonymousBoardRepositoryPort
from anonymous_board.domain.anonymous_board import AnonymousBoard
from anonymous_board.infrastructure.orm.anonymous_board_orm import AnonymousBoardORM
from config.database.session import get_db_session


class AnonymousBoardRepositoryImpl(AnonymousBoardRepositoryPort):
    def __init__(self):
        self.db: Session = get_db_session()

    def save(self, board: AnonymousBoard) -> AnonymousBoard:
        orm_board = AnonymousBoardORM(
            title=board.title,
            content=board.content,
        )
        self.db.add(orm_board)
        self.db.commit()
        self.db.refresh(orm_board)

        board.id = orm_board.id
        board.created_at = orm_board.created_at
        board.updated_at = orm_board.updated_at
        return board

    def get_by_id(self, board_id: int) -> Optional[AnonymousBoard]:
        orm_board = self.db.query(AnonymousBoardORM).filter(AnonymousBoardORM.id == board_id).first()
        if orm_board:
            board = AnonymousBoard(
                title=orm_board.title,
                content=orm_board.content,
            )
            board.id = orm_board.id
            board.created_at = orm_board.created_at
            board.updated_at = orm_board.updated_at
            return board
        return None

    def list_all(self) -> List[AnonymousBoard]:
        orm_boards = self.db.query(AnonymousBoardORM).all()
        boards = []
        for orm_board in orm_boards:
            board = AnonymousBoard(
                title=orm_board.title,
                content=orm_board.content,
            )
            board.id = orm_board.id
            board.created_at = orm_board.created_at
            board.updated_at = orm_board.updated_at
            boards.append(board)
        return boards

    def delete(self, board_id: int) -> None:
        self.db.query(AnonymousBoardORM).filter(AnonymousBoardORM.id == board_id).delete()
        self.db.commit()
