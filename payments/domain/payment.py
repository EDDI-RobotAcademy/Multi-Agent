from dataclasses import dataclass
from datetime import datetime

from payments.domain.payment_status import PaymentStatus


@dataclass
class Payment:
    order_id: str
    account_id: int
    amount: int
    status: PaymentStatus
    created_at: datetime | None = None