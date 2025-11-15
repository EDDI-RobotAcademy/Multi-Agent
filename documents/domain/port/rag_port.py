from abc import ABC, abstractmethod

class RAGPort(ABC):

    @abstractmethod
    def answer(self, query: str) -> str:
        """Return an answer using RAG (Retriever + Generator)."""
        pass
