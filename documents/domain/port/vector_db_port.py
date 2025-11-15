from abc import ABC, abstractmethod

class VectorDBPort(ABC):
    @abstractmethod
    def add_document(self, doc_id: str, content: str): ...

    @abstractmethod
    def search_similar(self, query: str, top_k: int = 5): ...
