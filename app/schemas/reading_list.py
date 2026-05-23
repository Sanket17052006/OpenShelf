from pydantic import BaseModel
from typing import Optional


class AddToList(BaseModel):
    ol_id: str
    title: str
    author: Optional[str] = None
    cover_url: Optional[str] = None


class ReadingListItemResponse(BaseModel):
    id: int
    ol_id: str
    title: str
    author: Optional[str] = None
    cover_url: Optional[str] = None

    class Config:
        from_attributes = True
