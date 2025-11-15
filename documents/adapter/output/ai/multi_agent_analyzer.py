# multi_agent_analyzer.py
from typing import Annotated, List
from langgraph.graph import StateGraph
from transformers import pipeline, AutoTokenizer
import asyncio
import fitz  # PyMuPDF
import math
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ---------------------------
# LangGraph state schema
# ---------------------------
class MyStateSchema:
    bullet_summary_done: bool = False
    abstract_summary_done: bool = False
    casual_summary_done: bool = False
    final_summary_done: bool = False
    answer_generated: bool = False


# ---------------------------
# PDF Reader
# ---------------------------
def read_pdf(file_path: str) -> str:
    doc = fitz.open(file_path)
    pages = []
    for page in doc:
        pages.append(page.get_text())
    return "\n".join(pages).strip()


# ---------------------------
# Token-based chunking
# ---------------------------
class TokenChunker:
    def __init__(self, tokenizer, max_input_tokens: int = 1024, margin_tokens: int = 50):
        self.tokenizer = tokenizer
        self.max_tokens = max_input_tokens
        self.margin = margin_tokens
        self.chunk_size = max(64, self.max_tokens - self.margin)

    def chunk_text(self, text: str) -> List[str]:
        token_ids = self.tokenizer.encode(text, add_special_tokens=False)
        if not token_ids:
            return []

        chunks = []
        total = len(token_ids)
        num_chunks = math.ceil(total / self.chunk_size)

        for i in range(num_chunks):
            start = i * self.chunk_size
            end = start + self.chunk_size
            chunk_ids = token_ids[start:end]
            chunk_text = self.tokenizer.decode(chunk_ids, skip_special_tokens=True)
            chunks.append(chunk_text.strip())

        return chunks


# ---------------------------
# MultiAgent Analyzer
# ---------------------------
class MultiAgentAnalyzer:
    def __init__(
        self,
        model_name: str = "facebook/bart-large-cnn",
        device: int = -1,
        encoder_max_tokens: int | None = None,
    ):
        logger.info("Initializing tokenizer and summarizer pipeline...")

        # ✅ 핵심 해결: fast tokenizer 제거 → Already borrowed 방지
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            use_fast=False
        )

        # ✅ summarizer 초기화
        self.summarizer = pipeline(
            "summarization",
            model=model_name,
            tokenizer=self.tokenizer,
            device=device
        )

        self.encoder_max_tokens = encoder_max_tokens or 1024

        # ✅ token chunker 생성
        self.chunker = TokenChunker(
            self.tokenizer,
            max_input_tokens=self.encoder_max_tokens,
            margin_tokens=50
        )

        # ✅ 핵심 해결: pipeline + tokenizer thread-safe 보장을 위해 concurrency=1
        self.semaphore = asyncio.Semaphore(1)

    # 안전한 truncate (fast tokenizer 제거로 안정성 향상)
    def _safe_truncate(self, text: str) -> str:
        ids = self.tokenizer.encode(
            text,
            truncation=True,
            max_length=self.chunker.chunk_size
        )
        return self.tokenizer.decode(ids, skip_special_tokens=True)

    async def _summarize_single_chunk(self, prompt: str, max_length: int, min_length: int) -> str:
        loop = asyncio.get_event_loop()

        def sync_call():
            try:
                # ✅ prompt 전체를 모델 입력 한도 이하로 강제 truncate
                safe_ids = self.tokenizer.encode(
                    prompt,
                    truncation=True,
                    max_length=900,  # ← BART 안정값 (1024보다 충분히 낮게)
                )
                safe_prompt = self.tokenizer.decode(safe_ids, skip_special_tokens=True)

                out = self.summarizer(
                    safe_prompt,
                    max_length=max_length,
                    min_length=min_length,
                    do_sample=False
                )
                if isinstance(out, list) and out and isinstance(out[0], dict):
                    return out[0].get("summary_text", "").strip()
                return str(out).strip()

            except Exception as e:
                logger.exception("Summarizer failed on chunk: %s", e)

                # ✅ fallback: 600 토큰까지 더 줄여서 재시도
                fallback_ids = self.tokenizer.encode(
                    prompt,
                    truncation=True,
                    max_length=600,
                )
                fallback_prompt = self.tokenizer.decode(fallback_ids, skip_special_tokens=True)

                out2 = self.summarizer(
                    fallback_prompt,
                    max_length=max_length,
                    min_length=min_length,
                    do_sample=False
                )
                return out2[0].get("summary_text", "").strip()

        async with self.semaphore:
            return await loop.run_in_executor(None, sync_call)

    async def summarize_token_chunks(self, text: str, prompt_type: str) -> str:
        if not text:
            return ""

        chunks = self.chunker.chunk_text(text)
        logger.info("Token chunks = %d", len(chunks))

        tasks = []
        for chunk in chunks:
            if prompt_type == "bullet":
                prompt = f"Summarize as bullet points:\n\n{chunk}"
                max_len, min_len = 180, 10
            elif prompt_type == "abstract":
                prompt = f"Write an academic abstract:\n\n{chunk}"
                max_len, min_len = 200, 40
            else:  # casual
                prompt = f"Write a casual summary:\n\n{chunk}"
                max_len, min_len = 160, 20

            tasks.append(self._summarize_single_chunk(prompt, max_len, min_len))

        results = await asyncio.gather(*tasks)
        return "\n".join([r for r in results if r.strip()])

    async def generate_final_summary(self, bullet: str, abstract: str, casual: str) -> str:
        prompt = (
            "Merge these summaries into one clear overview, avoiding repetition.\n\n"
            f"Bullet:\n{bullet}\n\nAbstract:\n{abstract}\n\nCasual:\n{casual}"
        )
        return await self._summarize_single_chunk(prompt, 300, 80)

    async def generate_qa(self, text: str, num_qa: int = 6) -> str:
        short_summary = await self._summarize_single_chunk(
            f"Summarize in 2–3 sentences:\n\n{text}",
            120, 30
        )

        prompt = (
            f"Generate {num_qa} Q&A pairs based on:\n\n"
            f"Summary:\n{short_summary}\n\n"
            f"Content excerpt:\n{text[:4000]}"
        )
        return await self._summarize_single_chunk(prompt, 300, 60)

    async def run(self, local_path: str):
        text_content = read_pdf(local_path)
        if not text_content:
            raise ValueError("PDF content empty")

        graph = StateGraph(Annotated[MyStateSchema, "reducer"])
        state = MyStateSchema()

        bullet, abstract, casual = await asyncio.gather(
            self.summarize_token_chunks(text_content, "bullet"),
            self.summarize_token_chunks(text_content, "abstract"),
            self.summarize_token_chunks(text_content, "casual"),
        )

        state.bullet_summary_done = True
        state.abstract_summary_done = True
        state.casual_summary_done = True

        final_summary = await self.generate_final_summary(bullet, abstract, casual)
        state.final_summary_done = True

        qa = await self.generate_qa(text_content)
        state.answer_generated = True

        return {
            "summaries": {
                "bullet": bullet,
                "abstract": abstract,
                "casual": casual,
            },
            "final_summary": final_summary,
            "answer": qa,
            "state": {
                "bullet_summary_done": state.bullet_summary_done,
                "abstract_summary_done": state.abstract_summary_done,
                "casual_summary_done": state.casual_summary_done,
                "final_summary_done": state.final_summary_done,
                "answer_generated": state.answer_generated,
            }
        }
