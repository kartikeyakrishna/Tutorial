from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from app.extensions import db

class UserProgress(db.Model):
    __tablename__ = 'user_progress'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    tutorial_id = Column(Integer, ForeignKey('tutorials.id'), nullable=False)
    completed_sections = Column(Text)
    completion_percentage = Column(Float, default=0.0)
    last_accessed = Column(DateTime)
    completed_at = Column(DateTime)
    user = relationship('User', back_populates='progress')
    tutorial = relationship('Tutorial', back_populates='progress')

class Bookmark(db.Model):
    __tablename__ = 'bookmarks'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    content_type = Column(String(32), nullable=False)
    content_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship('User', back_populates='bookmarks') 