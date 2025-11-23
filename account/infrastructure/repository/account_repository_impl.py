from typing import List

from sqlalchemy.orm import Session
from account.application.port.account_repository_port import AccountRepositoryPort
from account.domain.account import Account
from account.infrastructure.orm.account_orm import AccountORM
from config.database.session import get_db_session


class AccountRepositoryImpl(AccountRepositoryPort):
    def __init__(self):
        self.db: Session = get_db_session()

    def save(self, account: Account) -> Account:
        orm_account = AccountORM(
            email=account.email,
            nickname=account.nickname
        )
        self.db.add(orm_account)
        self.db.commit()
        self.db.refresh(orm_account)

        account.id = orm_account.id
        account.created_at = orm_account.created_at
        account.updated_at = orm_account.updated_at
        return account

    def find_by_email(self, email: str) -> Account | None:
        orm_account = self.db.query(AccountORM).filter(AccountORM.email == email).first()
        if orm_account is None:
            return None

        account = Account(
            email=orm_account.email,
            nickname=orm_account.nickname,
        )
        account.id = orm_account.id
        account.created_at = orm_account.created_at
        account.updated_at = orm_account.updated_at
        return account

    def find_all_by_id(self, ids: list[int]) -> List[Account]:
        orm_accounts = self.db.query(AccountORM).filter(AccountORM.id.in_(ids)).all()
        accounts: List[Account] = []
        for o in orm_accounts:
            account = Account(email=o.email, nickname=o.nickname)
            account.id = o.id
            account.created_at = o.created_at
            account.updated_at = o.updated_at
            accounts.append(account)
        return accounts

    def count(self) -> int:
        return self.db.query(AccountORM).count()
