from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.extensions import db

class Comment(db.Model):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    parent_type = Column(String(32), nullable=False)
    parent_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_edited = Column(Boolean, default=False)
    edited_at = Column(DateTime)
    author = relationship('User', back_populates='comments')

class Vote(db.Model):
    __tablename__ = 'votes'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    target_type = Column(String(32), nullable=False)
    target_id = Column(Integer, nullable=False)
    vote_type = Column(String(16), nullable=False)  # upvote/downvote
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship('User', back_populates='votes') 