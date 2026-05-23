from sqlalchemy import Column, Integer, String, ForeignKey

from app.database import Base


class ReadingListItem(Base):
    __tablename__ = "reading_list_items"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    ol_id = Column(String, nullable=False)
    title = Column(String, nullable=False)
    author = Column(String, nullable=True)
    cover_url = Column(String, nullable=True)
