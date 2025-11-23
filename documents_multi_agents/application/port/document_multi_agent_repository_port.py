from abc import ABC, abstractmethod
from documents_multi_agents.domain.document_agents import DocumentAgents

class DocumentMultiAgentRepositoryPort(ABC):

    @abstractmethod
    def find_by_doc_id(self, doc_id: int) -> DocumentAgents | None:
        pass

    @abstractmethod
    def save(self, agents: DocumentAgents) -> DocumentAgents:
        pass
