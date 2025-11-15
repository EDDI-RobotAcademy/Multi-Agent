from abc import ABC, abstractmethod

class SentimentAnalysisPort(ABC):

    @abstractmethod
    def analyze(self, text: str) -> dict:
        pass
