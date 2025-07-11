from sqlalchemy import Column, Integer, Enum, Text, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from enums.role import RoleEnum

from database.base import Base

class Messages(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(UUID(as_uuid=True), ForeignKey("chats.id", ondelete="CASCADE"))
    role = Column(Enum(RoleEnum), nullable=False)  
    content = Column(Text, nullable=False)
    token_count = Column(Integer, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    chat = relationship("Chats", back_populates="messages")