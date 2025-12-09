from fastapi import APIRouter, Depends, Cookie, HTTPException

from payments.adapter.input.web.request.payment_confirm_request import PaymentConfirmRequest
from payments.adapter.output.repository.payment_repository_impl import PaymentRepositoryImpl
from payments.domain.payment import Payment, PaymentStatus
from datetime import datetime

from utility.session_helper import get_current_user

payment_router = APIRouter(prefix="/payments", tags=["payments"])

@payment_router.post("/confirm")
async def confirm_payment(
    request: PaymentConfirmRequest,
    account_id: int = Depends(get_current_user),
    repo: PaymentRepositoryImpl = Depends(PaymentRepositoryImpl)
):

    payment = Payment(
        order_id=request.orderId,
        account_id=account_id,
        amount=request.amount,
        status=PaymentStatus.DONE,
        created_at=datetime.utcnow()
    )
    saved_payment = repo.save(payment)
    return {"message": "Payment confirmed", "orderId": saved_payment.order_id}