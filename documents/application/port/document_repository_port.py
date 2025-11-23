from abc import ABC, abstractmethod
from typing import List
from documents.domain.document import Document

class DocumentRepositoryPort(ABC):
    @abstractmethod
    def save(self, document: Document) -> Document:
        pass

    @abstractmethod
    def find_all(self) -> List[Document]:
        pass
