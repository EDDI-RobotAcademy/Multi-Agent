from fastapi import APIRouter, HTTPException

from documents_multi_agents.adapter.input.web.request.analyze_request import AnalyzeRequest
from documents_multi_agents.application.usecase.document_multi_agent_usecase import DocumentMultiAgentsUseCase

documents_multi_agents_router = APIRouter(tags=["documents_multi_agents"])

# Repositories & UseCase
usecase = DocumentMultiAgentsUseCase.getInstance()


@documents_multi_agents_router.post("/analyze")
async def analyze_document(request: AnalyzeRequest):
    try:
        agents = await usecase.analyze_document(request.doc_id, request.doc_url, request.question)
        return {
            "parsed_text": agents.parsed_text,
            "summaries": {
                "bullet": agents.bullet_summary,
                "abstract": agents.abstract_summary,
                "casual": agents.casual_summary,
                "final": agents.final_summary
            },
            "answer": agents.answer
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
