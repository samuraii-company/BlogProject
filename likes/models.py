from database.db import Base

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship


class Likes(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    post = Column(ForeignKey("posts.id", ondelete="CASCADE"))
    user = Column(ForeignKey("users.id", ondelete="CASCADE"))
    post_likes = relationship("Posts", back_populates="likes")
    like_author = relationship("Users", back_populates="likes")
