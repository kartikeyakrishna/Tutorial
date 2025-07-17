from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Enum, Table
from sqlalchemy.orm import relationship
from app.extensions import db

class Tutorial(db.Model):
    __tablename__ = 'tutorials'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    content = Column(Text)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    difficulty_level = Column(String(32))
    estimated_time = Column(Integer)
    language = Column(String(32))
    is_published = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    author = relationship('User', back_populates='tutorials')
    sections = relationship('TutorialSection', back_populates='tutorial', cascade='all, delete-orphan')
    progress = relationship('UserProgress', back_populates='tutorial')

class TutorialSection(db.Model):
    __tablename__ = 'tutorial_sections'
    id = Column(Integer, primary_key=True)
    tutorial_id = Column(Integer, ForeignKey('tutorials.id'), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text)
    order_index = Column(Integer)
    code_examples = Column(Text)
    tutorial = relationship('Tutorial', back_populates='sections')

class Article(db.Model):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    content = Column(Text)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    category = Column(String(64))
    tags = Column(String(255))
    is_featured = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    author = relationship('User', back_populates='articles')

class CodeSnippet(db.Model):
    __tablename__ = 'code_snippets'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    code = Column(Text, nullable=False)
    language = Column(String(32))
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    is_public = Column(Boolean, default=True)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    author = relationship('User', back_populates='code_snippets') 