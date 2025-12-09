from abc import ABC, abstractmethod
from payments.domain.payment import Payment

class PaymentRepositoryPort(ABC):
    @abstractmethod
    async def save(self, payment: Payment) -> None:
        pass
