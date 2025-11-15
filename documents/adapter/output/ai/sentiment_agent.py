# documents/adapter/output/ai/sentiment_agent.py
from transformers import pipeline
from documents.domain.port.sentiment_analysis_port import SentimentAnalysisPort

class SentimentAgent(SentimentAnalysisPort):
    """
    한국어 감정 분석용 에이전트 (로그인 필요 없는 공개 모델 사용)
    """

    def __init__(self):
        model_name = "nlpai-lab/korean-sentiment-analysis"

        try:
            self.analyzer = pipeline(
                "sentiment-analysis",
                model=model_name,
            )
        except Exception:
            # fallback: 영어 기본 모델
            self.analyzer = pipeline("sentiment-analysis")

    def analyze(self, text: str) -> dict:
        if not text:
            return {"label": "unknown", "score": 0.0}

        safe_text = text[:2000]

        try:
            result = self.analyzer(safe_text)
        except Exception:
            return {"label": "error", "score": 0.0}

        if isinstance(result, list) and len(result) > 0:
            return result[0]

        return {"label": "unknown", "score": 0.0}
