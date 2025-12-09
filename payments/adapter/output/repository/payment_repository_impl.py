from datetime import datetime

from config.database.session import SessionLocal
from payments.domain.payment import Payment
from payments.domain.port.toss_payment_port import PaymentRepositoryPort
from payments.infrastructure.orm.payment_orm import PaymentORM


class PaymentRepositoryImpl(PaymentRepositoryPort):
    def __init__(self):
        self.db = SessionLocal()

    def save(self, payment: Payment) -> Payment:
        orm = self.db.get(PaymentORM, payment.order_id)
        if orm is None:
            orm = PaymentORM(
                order_id=payment.order_id,
                account_id=payment.account_id,
                amount=payment.amount,
                status=payment.status.value,
                created_at=datetime.utcnow(),
            )
            self.db.add(orm)
            self.db.commit()
            self.db.refresh(orm)
        else:
            orm.status = payment.status.value
            self.db.commit()
            self.db.refresh(orm)

        payment.created_at = orm.created_at
        return payment
