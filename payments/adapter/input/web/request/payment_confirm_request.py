from pydantic import BaseModel


class PaymentConfirmRequest(BaseModel):
    paymentKey: str
    orderId: str
    amount: int