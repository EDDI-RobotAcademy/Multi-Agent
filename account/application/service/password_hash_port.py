from abc import ABC, abstractmethod

class IPasswordHasher(ABC):
    @abstractmethod
    def hash(self, password: str) -> str:
        """주어진 비밀번호 문자열을 해싱하여 반환합니다."""
        pass

    @abstractmethod
    def verify(self, plain_password: str, hashed_password: str) -> bool:
        """
        주어진 평문 비밀번호와 해싱된 비밀번호가 일치하는지 검증합니다.
        """
        pass