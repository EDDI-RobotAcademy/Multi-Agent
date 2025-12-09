# payments/application/usecase/confirm_payment_usecase.py
import os
import httpx
from payments.domain.payment import Payment, PaymentStatus
from payments.domain.port.toss_payment_port import PaymentRepositoryPort

TOSS_SECRET_KEY = os.environ.get("TOSS_SECRET_KEY")

class ConfirmPaymentUseCase:
    def __init__(self, payment_repo: PaymentRepositoryPort):
        self.payment_repo = payment_repo

    async def execute(self, payment_key: str, order_id: str, amount: int) -> Payment:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.tosspayments.com/v1/payments/confirm",
                json={"paymentKey": payment_key, "orderId": order_id, "amount": amount},
                headers={"Authorization": f"Basic {TOSS_SECRET_KEY}"},
                timeout=10,
            )
            res_data = response.json()

        status = PaymentStatus.DONE if res_data.get("status") == "DONE" else PaymentStatus.FAILED
        payment = Payment(order_id=order_id, amount=amount, status=status)

        await self.payment_repo.save(payment)
        return payment
