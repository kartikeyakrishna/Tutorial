from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.extensions import db

class ActivityLog(db.Model):
    __tablename__ = 'activity_logs'
    id = Column(Integer, primary_key=True)
    session_id = Column(String(128), index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    interaction_type = Column(String(64))
    content = Column(Text)
    activity_metadata = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship('User', back_populates='activity_logs') 