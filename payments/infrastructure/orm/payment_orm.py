from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime
from config.database.session import Base

class PaymentORM(Base):
    __tablename__ = "payment"

    order_id = Column(String, primary_key=True, index=True)
    account_id = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False)
    status = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
