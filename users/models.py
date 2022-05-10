from database.db import Base

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship

from datetime import datetime


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String(100))
    email = Column(String(100))
    password = Column(String(100))
    is_stuff = Column(Boolean, default=False)
    join_at = Column(DateTime, default=datetime.now)
    posts = relationship("Posts", back_populates="post_author")
    likes = relationship("Likes", back_populates="like_author")
    comments = relationship("Comments", back_populates="comment_author")
