from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from config.database.session import Base

class BoardORM(Base):
    __tablename__ = "board"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(String(2000), nullable=False)
    author_id = Column(Integer, ForeignKey("account.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
