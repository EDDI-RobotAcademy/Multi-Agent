from fastapi import APIRouter, UploadFile, File, Depends

from documents.adapter.input.web.request.rag_query_request import RAGQueryRequest
from documents.adapter.input.web.request.sentiment_request import SentimentRequest
from documents.application.factory.analyze_document_usecase_factory import get_analyze_document_usecase
from documents.application.factory.rag_query_usecase_factory import get_rag_query_usecase
from documents.application.factory.sentiment_analysis_usecase_factory import get_sentiment_analysis_usecase
from documents.application.factory.upload_file_usecase_factory import get_upload_document_usecase

documentRouter = APIRouter()

@documentRouter.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    usecase = Depends(get_upload_document_usecase)
):
    result = usecase.execute(file.file, file.filename)
    return {"url": result}

@documentRouter.post("/analysis/{document_id}")
async def analyze_document(
    document_id: int,
    usecase = Depends(get_analyze_document_usecase)
):
    result = await usecase.execute(document_id)
    return {"result": result}

@documentRouter.post("/rag/query")
async def rag_query(
    request: RAGQueryRequest,
    usecase = Depends(get_rag_query_usecase)
):
    result = usecase.ask(request.query)
    return {"result": result}

@documentRouter.post("/sentiment")
async def sentiment_analysis(
    request: SentimentRequest,
    usecase = Depends(get_sentiment_analysis_usecase)
):
    result = usecase.analyze(request.text)
    return {"result": result}
