from database.db import Base

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from users.models import Users


class Posts(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String(100))
    text = Column(String(3000))
    likes_count = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now)
    author = Column(ForeignKey("users.id", ondelete="CASCADE"))
    post_author = relationship(Users, back_populates="posts")
    likes = relationship("Likes", back_populates="post_likes")
    comments = relationship("Comments", back_populates="post_comments")
