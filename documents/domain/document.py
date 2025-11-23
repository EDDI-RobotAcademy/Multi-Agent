from typing import Optional
from datetime import datetime

class Document:
    def __init__(self, file_name: str, s3_key: str, uploader_id: int):
        self.id: Optional[int] = None
        self.file_name = file_name
        self.s3_key = s3_key
        self.uploader_id = uploader_id
        self.uploaded_at: datetime = datetime.utcnow()
        self.updated_at: datetime = datetime.utcnow()

    @classmethod
    def create(cls, file_name: str, s3_key: str, uploader_id: int) -> "Document":
        if not file_name or not s3_key:
            raise ValueError("file_name과 s3_key는 필수입니다")
        return cls(file_name, s3_key, uploader_id)
