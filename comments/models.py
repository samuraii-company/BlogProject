from database.db import Base

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from users.models import Users
from posts.models import Posts


class Comments(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    text = Column(String(3000))
    created_at = Column(DateTime, default=datetime.now)
    author = Column(ForeignKey("users.id", ondelete="CASCADE"))
    post = Column(ForeignKey("posts.id", ondelete="CASCADE"))
    post_comments = relationship(Posts, back_populates="comments")
    comment_author = relationship(Users, back_populates="comments")
