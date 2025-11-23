from typing import List, Optional

from account.application.port.account_repository_port import AccountRepositoryPort
from account.domain.account import Account


class AccountUseCase:
    def __init__(self, account_repository: AccountRepositoryPort):
        self.repo = account_repository

    def create_or_get_account(self, email: str, nickname: str | None):
        account = self.repo.find_by_email(email)
        if account:
            return account

        if not nickname:
            total = self.repo.count()
            nickname = f"anonymous{total + 1}"

        account = Account(email=email, nickname=nickname)
        return self.repo.save(account)

    def get_account_by_id(self, account_id: int) -> Optional[Account]:
        accounts = self.get_accounts_by_ids([account_id])
        return accounts[0] if accounts else None

    def get_accounts_by_ids(self, ids: list[int]) -> List[Account]:

        if not ids:
            return []

        return self.repo.find_all_by_id(ids)
