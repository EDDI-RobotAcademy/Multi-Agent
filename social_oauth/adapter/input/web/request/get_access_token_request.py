from pydantic import BaseModel

class GetAccessTokenRequest(BaseModel):
    state: str
    code: str
    