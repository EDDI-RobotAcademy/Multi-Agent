from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from config.database.session import Base

class DocumentORM(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String(255), nullable=False)
    s3_key = Column(String(255), nullable=False)
    uploader_id = Column(Integer, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
