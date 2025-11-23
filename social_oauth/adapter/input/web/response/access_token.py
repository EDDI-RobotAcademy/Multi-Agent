from pydantic import BaseModel


class AccessToken(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str | None = None