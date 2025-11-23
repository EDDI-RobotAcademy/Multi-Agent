from sqlalchemy import Column, Integer, String, DateTime

from datetime import datetime

from config.database.session import Base


# @Entity
# orm 붙어 있는 것은
# 실제 Layered Architecture에서는 entity에 해당함.
class AnonymousBoardORM(Base):
    __tablename__ = "anonymous_board"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(String(2000), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
