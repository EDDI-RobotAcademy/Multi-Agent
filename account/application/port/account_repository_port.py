from typing import Optional, List
from abc import ABC, abstractmethod
from account.domain.account import Account

class AccountRepositoryPort(ABC):

    @abstractmethod
    def save(self, account: Account) -> Account:
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[Account]:
        pass

    @abstractmethod
    def find_all_by_id(self, ids: list[int]) -> List[Account]:
        pass

    @abstractmethod
    def count(self) -> int:
        pass
