from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, TIMESTAMP, text
from sqlalchemy.orm import relationship
from app.database import Base


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String,  nullable=False)
    description = Column(String, nullable=False)
    is_published = Column(Boolean, server_default='FALSE')
    review = Column(Integer, nullable=True)
    create_at = Column(TIMESTAMP(timezone=True),
                       nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey(
        'users.id', ondelete="CASCADE"),  nullable=False)

    owner = relationship('User')


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    create_at = Column(TIMESTAMP(timezone=True),
                       nullable=False, server_default=text('now()'))

 
class Vote(Base):
    __tablename__ = 'votes'
    id = Column(Integer, primary_key=True, nullable=False)
    post_id = Column(Integer, ForeignKey(
        'posts.id', ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey(
        'users.id', ondelete="CASCADE"), nullable=False)
