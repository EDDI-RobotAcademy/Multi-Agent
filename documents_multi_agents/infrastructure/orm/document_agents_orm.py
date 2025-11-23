from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime
from config.database.session import Base

class DocumentAgentsORM(Base):
    __tablename__ = "documents_multi_agents"

    id = Column(Integer, primary_key=True, index=True)
    doc_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    doc_url = Column(String(255), nullable=False, unique=True)
    parsed_text = Column(Text, nullable=True)
    bullet_summary = Column(Text, nullable=True)
    abstract_summary = Column(Text, nullable=True)
    casual_summary = Column(Text, nullable=True)
    final_summary = Column(Text, nullable=True)
    answer = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
