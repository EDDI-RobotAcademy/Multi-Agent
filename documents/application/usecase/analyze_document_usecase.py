from documents.domain.entity.document import Document

class AnalyzeDocumentUseCase:
    def __init__(self, document_repo, storage_adapter, analyzer, vector_db_adapter):
        self.document_repo = document_repo
        self.storage_adapter = storage_adapter
        self.analyzer = analyzer
        self.vector_db = vector_db_adapter

    async def execute(self, document_id: int):
        # ✅ 1. DB에서 문서 조회
        document: Document = self.document_repo.find_by_id(document_id)
        if not document:
            raise ValueError(f"Document with id={document_id} not found")

        s3_url = str(document.path.s3_url)
        print(f"Downloading from S3: {s3_url}")

        # ✅ 2. S3에서 로컬 다운로드
        local_path = await self.storage_adapter.download_file(s3_url)
        print(f"Downloaded to: {local_path}")

        # ✅ 3. 멀티 에이전트 분석 실행
        result = await self.analyzer.run(local_path)

        # ✅ 4. 분석된 요약을 모두 합쳐 RAG 벡터 DB에 저장
        # bullet/abstract/casual 요약 필드가 있다고 가정
        summaries = result.get("summaries", {})

        # ✅ 빈 텍스트 방지
        full_text = "\n".join([
            summaries.get("bullet", ""),
            summaries.get("abstract", ""),
            summaries.get("casual", "")
        ]).strip()

        if full_text:
            print(f"🔍 Adding document {document_id} to vector DB...")
            self.vector_db.add_document(str(document_id), full_text)

        return result
