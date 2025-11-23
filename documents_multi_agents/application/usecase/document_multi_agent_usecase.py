import asyncio

from documents.infrastructure.repository.document_repository_impl import DocumentRepositoryImpl
from documents_multi_agents.domain.document_agents import DocumentAgents
from documents_multi_agents.infrastructure.external.download_agent import download_document, get_cache_filename
from documents_multi_agents.infrastructure.external.parse_agent import parse_document
from documents_multi_agents.infrastructure.external.summarizers import bullet_summarizer, abstract_summarizer, \
    casual_summarizer, consensus_summarizer, answer_agent

from documents_multi_agents.infrastructure.repository.document_multi_agent_repository_impl import \
    DocumentsMultiAgentsRepositoryImpl


class DocumentMultiAgentsUseCase:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.doc_repo = DocumentRepositoryImpl.getInstance()
            cls.__instance.agents_repo = DocumentsMultiAgentsRepositoryImpl.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    async def analyze_document(self, doc_id: int, doc_url: str, question: str) -> DocumentAgents:
        # 이미 저장된 agents가 있는지 확인
        agents = self.agents_repo.find_by_doc_id(doc_id)
        if not agents:
            agents = DocumentAgents(doc_id=doc_id, doc_url=doc_url)

        # 다운로드
        content = await download_document(doc_url)
        cache_path = get_cache_filename(doc_url)

        # 파싱
        parsed_text = parse_document(content, cache_path)
        agents.update_parsed_text(parsed_text)

        # 병렬 요약
        bullet, abstract, casual = await asyncio.gather(
            bullet_summarizer(parsed_text),
            abstract_summarizer(parsed_text),
            casual_summarizer(parsed_text)
        )

        final_summary = await consensus_summarizer([bullet, abstract, casual])
        answer = await answer_agent(final_summary, question)

        agents.update_summaries(bullet=bullet, abstract=abstract, casual=casual, final=final_summary)
        agents.set_answer(answer)

        # DB 저장
        self.agents_repo.save(agents)

        return agents
