from pydantic import BaseModel

class UpdateBoardRequest(BaseModel):
    title: str
    content: str
