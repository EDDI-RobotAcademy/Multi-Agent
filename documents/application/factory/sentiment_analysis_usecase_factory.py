from documents.adapter.output.ai.sentiment_agent import SentimentAgent
from documents.application.usecase.sentiment_analysis_usecase import SentimentAnalysisUseCase


def get_sentiment_analysis_usecase():
    sentiment_agent = SentimentAgent()
    return SentimentAnalysisUseCase(sentiment_agent)
