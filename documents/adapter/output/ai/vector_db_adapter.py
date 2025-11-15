from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from documents.domain.port.vector_db_port import VectorDBPort


class FAISSVectorDBAdapter(VectorDBPort):
    def __init__(self):
        model_name = "sentence-transformers/all-MiniLM-L6-v2"
        self.embedding = HuggingFaceEmbeddings(model_name=model_name)

        # dummy로 초기 인덱스 생성
        self.db = FAISS.from_texts(["dummy"], self.embedding)

        # ✅ 실제 존재하는 인덱스 ID만 삭제
        try:
            if len(self.db.index_to_docstore_id) > 0:
                # key = 실제 FAISS 인덱스 번호 (0,1,2,...)
                faiss_index_id = list(self.db.index_to_docstore_id.keys())[0]
                self.db.delete([faiss_index_id])
        except Exception as e:
            print("Dummy delete skipped:", e)

    def add_document(self, doc_id: str, content: str):
        self.db.add_texts([content], ids=[doc_id])

    def search_similar(self, query: str, top_k: int = 5):
        return self.db.similarity_search(query, k=top_k)

    def as_retriever(self):
        return self.db.as_retriever()
