from documents.adapter.output.ai.vector_db_adapter import FAISSVectorDBAdapter
from documents.adapter.output.ai.rag_pipeline_adapter import RAGPipelineAdapter
from documents.application.usecase.rag_query_usecase import RAGQueryUsecase


def get_rag_query_usecase():
    vector_db = FAISSVectorDBAdapter()
    rag_adapter = RAGPipelineAdapter(vector_db)
    return RAGQueryUsecase(rag_adapter)
