from typing import List
from sqlalchemy.orm import Session

from config.database.session import SessionLocal
from documents.application.port.document_repository_port import DocumentRepositoryPort
from documents.domain.document import Document
from documents.infrastructure.orm.document_orm import DocumentORM


class DocumentRepositoryImpl(DocumentRepositoryPort):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def save(self, document: Document) -> Document:

        db: Session = SessionLocal()
        try:
            db_obj = DocumentORM(
                file_name=document.file_name,
                s3_key=document.s3_key,
                uploader_id=document.uploader_id,
            )
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)

            # DB에서 받은 id와 timestamp를 도메인 객체에 반영
            document.id = db_obj.id
            document.uploaded_at = db_obj.uploaded_at
            document.updated_at = db_obj.updated_at
        finally:
            db.close()

        return document

    def find_all(self) -> List[Document]:
        """
        DB에 있는 모든 문서를 도메인 객체로 반환
        """
        db: Session = SessionLocal()
        documents: List[Document] = []
        try:
            db_objs = db.query(DocumentORM).all()
            for obj in db_objs:
                doc = Document(
                    file_name=obj.file_name,
                    s3_key=obj.s3_key,
                    uploader_id=obj.uploader_id
                )
                doc.id = obj.id
                doc.uploaded_at = obj.uploaded_at
                doc.updated_at = obj.updated_at
                documents.append(doc)
        finally:
            db.close()

        return documents
