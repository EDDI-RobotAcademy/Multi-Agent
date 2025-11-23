from typing import List
from documents.domain.document import Document
from documents.infrastructure.repository.document_repository_impl import DocumentRepositoryImpl


class DocumentUseCase:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.repository = DocumentRepositoryImpl.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def register_document(self, file_name: str, s3_key: str, uploader_id: int) -> Document:
        doc = Document.create(file_name, s3_key, uploader_id)
        return self.repository.save(doc)

    def list_documents(self) -> List[Document]:
        return self.repository.find_all()
