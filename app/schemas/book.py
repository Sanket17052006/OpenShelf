from pydantic import BaseModel
from typing import Optional


class BookSearchResult(BaseModel):
    ol_id: str
    title: str
    author: Optional[str] = None
    first_publish_year: Optional[int] = None
    cover_url: Optional[str] = None


class BookDetail(BaseModel):
    ol_id: str
    title: str
    author: Optional[str] = None
    description: Optional[str] = None
    first_publish_year: Optional[int] = None
    cover_url: Optional[str] = None
    subjects: list[str] = []
    pages: Optional[int] = None
