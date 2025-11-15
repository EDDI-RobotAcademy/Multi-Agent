from documents.adapter.output.ai.vector_db_adapter import FAISSVectorDBAdapter
from documents.adapter.output.persistence.document_repository_adapter import DocumentRepositoryAdapter
from documents.adapter.output.storage.s3_storage_adapter import S3StorageAdapter
from documents.adapter.output.ai.multi_agent_analyzer import MultiAgentAnalyzer
from documents.application.usecase.analyze_document_usecase import AnalyzeDocumentUseCase
import os


def get_analyze_document_usecase():
    bucket_name = os.getenv("AWS_S3_BUCKET")
    document_repo = DocumentRepositoryAdapter()
    storage_adapter = S3StorageAdapter(bucket_name)
    analyzer = MultiAgentAnalyzer()
    vector_db_adapter = FAISSVectorDBAdapter()

    return AnalyzeDocumentUseCase(
        document_repo,
        storage_adapter,
        analyzer,
        vector_db_adapter
    )
