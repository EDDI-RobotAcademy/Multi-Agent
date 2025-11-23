from pydantic import BaseModel


class RegisterDocumentRequest(BaseModel):
    file_name: str
    s3_key: str
