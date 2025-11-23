import asyncio
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

SUMMARIZE_MODEL = "facebook/bart-large-cnn"
summarize_tokenizer = AutoTokenizer.from_pretrained(SUMMARIZE_MODEL)
summarize_model = AutoModelForSeq2SeqLM.from_pretrained(SUMMARIZE_MODEL)
summarize_pipeline = pipeline("summarization", model=summarize_model, tokenizer=summarize_tokenizer)

QA_MODEL = "google/flan-t5-large"
qa_tokenizer = AutoTokenizer.from_pretrained(QA_MODEL)
qa_model = AutoModelForSeq2SeqLM.from_pretrained(QA_MODEL)
qa_pipeline = pipeline("text2text-generation", model=qa_model, tokenizer=qa_tokenizer, framework="pt")

async def bullet_summarizer(text: str) -> str:
    # 지침을 Prompt에서 제거하고, 실제 텍스트만 요약
    return summarize_pipeline(text, max_length=200, min_length=50, do_sample=False)[0]["summary_text"]

async def abstract_summarizer(text: str) -> str:
    return summarize_pipeline(text, max_length=250, min_length=100, do_sample=False)[0]["summary_text"]

async def casual_summarizer(text: str) -> str:
    return summarize_pipeline(text, max_length=200, min_length=50, do_sample=False)[0]["summary_text"]

async def consensus_summarizer(summaries: list[str]) -> str:
    # 이미 요약된 핵심 텍스트만 합치기
    joined = "\n".join(s for s in summaries if s)
    return summarize_pipeline(joined, max_length=250, min_length=100, do_sample=False)[0]["summary_text"]

async def answer_agent(summary: str, question: str = "Summarize the text in English") -> str:
    # QA 모델도 Prompt 문구 없이 summary만 Context로 사용
    context = summary[:2000]  # 길면 자르기
    prompt = f"Context:\n{context}\nQuestion: {question}\nAnswer:"
    return await asyncio.to_thread(lambda: qa_pipeline(prompt, max_new_tokens=150)[0]["generated_text"].strip())
