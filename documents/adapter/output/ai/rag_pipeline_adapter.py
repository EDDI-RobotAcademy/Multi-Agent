import unicodedata
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from documents.domain.port.rag_port import RAGPort


# 하드코딩 문서
RAG_BASE_DOCS = [
    """
    도메인 분리 기준:
    1. 변경 이유가 다르면 분리한다.
    2. 비즈니스 규칙은 도메인에만 있어야 한다.
    3. 인프라(저장소, 외부 API)가 도메인을 참조하면 안 된다.
    4. 도메인 객체는 서로 과도하게 의존하면 안 된다.
    """,

    """
    도메인 설계 원칙:
    1. 고수준 정책과 저수준 구현을 분리한다.
    2. 도메인 서비스는 도메인 로직만 담당한다.
    3. 애플리케이션 서비스는 도메인을 조합하는 역할이다.
    4. 도메인은 기술 세부 사항을 몰라야 한다.
    """,

    """
    도메인 분리 실수:
    1. 도메인에 저장소 로직을 넣는 것.
    2. 엔티티/밸류가 너무 많은 기능을 가지는 것.
    3. 유틸리티나 헬퍼가 비즈니스 규칙을 알게 되는 것.
    4. CQRS에서 Read/Write 모델이 섞여버리는 것.
    """
]


def clean_text(text: str) -> str:
    if not isinstance(text, str):
        text = str(text)
    text = unicodedata.normalize("NFKC", text)
    text = "".join(ch for ch in text if ch.isprintable())
    return text.strip()


class RAGPipelineAdapter(RAGPort):
    def __init__(self, vector_db_adapter):
        self.vector_db = vector_db_adapter
        self.retriever = vector_db_adapter.as_retriever()

        # ✅ 한국어 T5 모델로 변경 (강력)
        model_name = "lcw99/t5-large-korean-text-summary"

        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

        self.llm = pipeline(
            "text2text-generation",
            model=model,
            tokenizer=tokenizer,
            max_length=256,
            num_beams=5,
            device=-1  # CPU
        )

    def _safe_retrieve_faiss(self, query: str) -> str:
        try:
            docs = self.retriever.invoke(query)
            if isinstance(docs, list):
                return "\n\n".join(
                    clean_text(d.page_content) if hasattr(d, "page_content") else clean_text(str(d))
                    for d in docs
                )
            if hasattr(docs, "page_content"):
                return clean_text(d.page_content)
            return clean_text(str(docs))
        except:
            return ""

    def _search_hardcoded_docs(self, query: str) -> str:
        q = query.lower()
        result = []
        for doc in RAG_BASE_DOCS:
            if "도메인" in doc or "분리" in doc or "설계" in doc:
                result.append(doc)
        return "\n\n".join(result)

    def answer(self, query: str) -> str:
        context = "\n\n".join([
            self._safe_retrieve_faiss(query),
            self._search_hardcoded_docs(query)
        ]).strip()

        if not context:
            return "관련된 정보를 찾을 수 없습니다."

        prompt = f"""
        아래 내용을 기반으로 질문에 답하세요.

        [Context]
        {context}

        [Question]
        {query}

        자연스럽고 명확한 한국어로 설명하시오.
        """

        out = self.llm(prompt)[0]["generated_text"]
        return clean_text(out)

    def query(self, query: str) -> str:
        return self.answer(query)
