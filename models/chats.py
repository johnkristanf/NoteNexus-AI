from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from models.messages import Messages
import uuid

from database.base import Base

class Chats(Base):
    __tablename__ = 'chats'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    title = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    messages = relationship(Messages, back_populates="chat", cascade="all, delete-orphan")