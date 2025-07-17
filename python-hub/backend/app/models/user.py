from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from app.extensions import db

class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(64), unique=True, nullable=False, index=True)
    password_hash = Column(String(128), nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    role = Column(String(32), default='user', index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    profile = relationship('UserProfile', uselist=False, back_populates='user', cascade='all, delete-orphan')
    preferences = relationship('UserPreferences', uselist=False, back_populates='user', cascade='all, delete-orphan')
    tutorials = relationship('Tutorial', back_populates='author')
    articles = relationship('Article', back_populates='author')
    code_snippets = relationship('CodeSnippet', back_populates='author')
    comments = relationship('Comment', back_populates='author')
    votes = relationship('Vote', back_populates='user')
    progress = relationship('UserProgress', back_populates='user')
    bookmarks = relationship('Bookmark', back_populates='user')
    activity_logs = relationship('ActivityLog', back_populates='user')

class UserProfile(db.Model):
    __tablename__ = 'user_profiles'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    display_name = Column(String(128))
    bio = Column(Text)
    avatar_url = Column(String(512))
    github_username = Column(String(64))
    learning_streak = Column(Integer, default=0)
    total_tutorials_completed = Column(Integer, default=0)
    user = relationship('User', back_populates='profile')

class UserPreferences(db.Model):
    __tablename__ = 'user_preferences'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    theme = Column(String(32), default='light')
    email_notifications = Column(Boolean, default=True)
    language_preference = Column(String(32), default='en')
    user = relationship('User', back_populates='preferences') 