from fastapi import APIRouter, Depends, Query, HTTPException

from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.book import BookSearchResult, BookDetail
from app.services import openlibrary

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/search", response_model=list[BookSearchResult])
async def search(
    q: str = Query(..., description="Search by title, author, or subject"),
    limit: int = Query(10, ge=1, le=50),
    current_user: User = Depends(get_current_user),
):
    return await openlibrary.search_books(q, limit)


@router.get("/{ol_id}", response_model=BookDetail)
async def detail(
    ol_id: str,
    current_user: User = Depends(get_current_user),
):
    book = await openlibrary.get_book_detail(ol_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book
