from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.reading_list import ReadingListItem
from app.schemas.reading_list import AddToList, ReadingListItemResponse

router = APIRouter(prefix="/list", tags=["reading list"])


@router.post("/add", response_model=ReadingListItemResponse, status_code=status.HTTP_201_CREATED)
def add_to_list(
    body: AddToList,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    existing = (
        db.query(ReadingListItem)
        .filter(
            ReadingListItem.user_id == current_user.id,
            ReadingListItem.ol_id == body.ol_id,
        )
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book already in your reading list",
        )

    item = ReadingListItem(
        user_id=current_user.id,
        ol_id=body.ol_id,
        title=body.title,
        author=body.author,
        cover_url=body.cover_url,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("", response_model=list[ReadingListItemResponse])
def get_list(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return (
        db.query(ReadingListItem)
        .filter(ReadingListItem.user_id == current_user.id)
        .all()
    )


@router.delete("/{ol_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_from_list(
    ol_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    item = (
        db.query(ReadingListItem)
        .filter(
            ReadingListItem.user_id == current_user.id,
            ReadingListItem.ol_id == ol_id,
        )
        .first()
    )
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found in your reading list",
        )
    db.delete(item)
    db.commit()
