class RAGQueryUsecase:
    def __init__(self, rag_service):
        self.rag_service = rag_service

    def ask(self, query: str) -> str:
        return self.rag_service.query(query)
