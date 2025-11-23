from typing import Optional

class DocumentAgents:
    def __init__(
        self,
        doc_id: int,
        doc_url: Optional[str] = None,
        parsed_text: Optional[str] = None,
        bullet_summary: Optional[str] = None,
        abstract_summary: Optional[str] = None,
        casual_summary: Optional[str] = None,
        final_summary: Optional[str] = None,
        answer: Optional[str] = None,
    ):
        self.doc_id = doc_id
        self.doc_url = doc_url
        self.parsed_text = parsed_text
        self.bullet_summary = bullet_summary
        self.abstract_summary = abstract_summary
        self.casual_summary = casual_summary
        self.final_summary = final_summary
        self.answer = answer

    def update_parsed_text(self, text: str):
        self.parsed_text = text

    def update_summaries(
        self,
        bullet: Optional[str] = None,
        abstract: Optional[str] = None,
        casual: Optional[str] = None,
        final: Optional[str] = None
    ):
        if bullet is not None:
            self.bullet_summary = bullet
        if abstract is not None:
            self.abstract_summary = abstract
        if casual is not None:
            self.casual_summary = casual
        if final is not None:
            self.final_summary = final

    def set_answer(self, answer: str):
        self.answer = answer
