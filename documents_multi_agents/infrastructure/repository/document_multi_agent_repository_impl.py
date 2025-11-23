from documents_multi_agents.application.port.document_multi_agent_repository_port import \
    DocumentMultiAgentRepositoryPort
from documents_multi_agents.domain.document_agents import DocumentAgents
from documents_multi_agents.infrastructure.orm.document_agents_orm import DocumentAgentsORM
from config.database.session import SessionLocal

class DocumentsMultiAgentsRepositoryImpl(DocumentMultiAgentRepositoryPort):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.db = SessionLocal()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def find_by_doc_id(self, doc_id: int) -> DocumentAgents | None:
        orm = self.db.query(DocumentAgentsORM).filter(DocumentAgentsORM.doc_id == doc_id).first()
        if not orm:
            return None
        agents = DocumentAgents(
            doc_id=orm.doc_id,
            doc_url=orm.doc_url,
            parsed_text=orm.parsed_text,
            bullet_summary=orm.bullet_summary,
            abstract_summary=orm.abstract_summary,
            casual_summary=orm.casual_summary,
            final_summary=orm.final_summary,
            answer=orm.answer
        )
        return agents

    def save(self, agents: DocumentAgents) -> DocumentAgents:
        orm = self.db.query(DocumentAgentsORM).filter(DocumentAgentsORM.doc_id == agents.doc_id).first()
        if orm:
            orm.doc_url = agents.doc_url
            orm.parsed_text = agents.parsed_text
            orm.bullet_summary = agents.bullet_summary
            orm.abstract_summary = agents.abstract_summary
            orm.casual_summary = agents.casual_summary
            orm.final_summary = agents.final_summary
            orm.answer = agents.answer
        else:
            orm = DocumentAgentsORM(
                doc_id=agents.doc_id,
                doc_url=agents.doc_url,
                parsed_text=agents.parsed_text,
                bullet_summary=agents.bullet_summary,
                abstract_summary=agents.abstract_summary,
                casual_summary=agents.casual_summary,
                final_summary=agents.final_summary,
                answer=agents.answer
            )
            self.db.add(orm)
        self.db.commit()
        self.db.refresh(orm)
        return agents
