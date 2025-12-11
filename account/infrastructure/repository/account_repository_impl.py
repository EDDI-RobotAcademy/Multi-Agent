from typing import List
from sqlalchemy.orm import Session
from account.application.port.account_repository_port import AccountRepositoryPort
from account.domain.account import Account
from account.infrastructure.orm.account_orm import AccountORM
from config.database.session import SessionLocal


class AccountRepositoryImpl(AccountRepositoryPort):

    def save(self, account: Account) -> Account:
        db: Session = SessionLocal()
        try:
            orm = AccountORM(
                email=account.email,
                nickname=account.nickname
            )
            db.add(orm)
            db.commit()
            db.refresh(orm)

            account.id = orm.id
            account.created_at = orm.created_at
            account.updated_at = orm.updated_at

            return account

        except:
            db.rollback()
            raise
        finally:
            db.close()

    def find_by_email(self, email: str) -> Account | None:
        db: Session = SessionLocal()
        try:
            orm = db.query(AccountORM).filter(AccountORM.email == email).first()
            if orm is None:
                return None

            account = Account(
                email=orm.email,
                nickname=orm.nickname
            )
            account.id = orm.id
            account.created_at = orm.created_at
            account.updated_at = orm.updated_at

            return account

        finally:
            db.close()

    def find_all_by_id(self, ids: list[int]) -> List[Account]:
        db: Session = SessionLocal()
        try:
            orms = db.query(AccountORM).filter(AccountORM.id.in_(ids)).all()
            accounts: List[Account] = []

            for o in orms:
                acc = Account(email=o.email, nickname=o.nickname)
                acc.id = o.id
                acc.created_at = o.created_at
                acc.updated_at = o.updated_at
                accounts.append(acc)

            return accounts

        finally:
            db.close()

    def count(self) -> int:
        db: Session = SessionLocal()
        try:
            return db.query(AccountORM).count()
        finally:
            db.close()
