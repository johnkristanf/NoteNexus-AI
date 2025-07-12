from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from models.messages import Messages
from schema.messages import MessagesCreate

class MessagesRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def create_message(self, message_data: MessagesCreate) -> Messages:
        new_message = Messages(**message_data.model_dump())
        self.db.add(new_message)
        self.db.commit()
        self.db.refresh(new_message)
        return new_message
    
    
    
    def get_messages_by_chat_id(self, chat_id: UUID) -> List[Messages]:
        return (
            self.db.query(Messages)
            .filter(Messages.chat_id == chat_id)
            .order_by(Messages.created_at.asc())  # Optional: sorts chronologically
            .all()
        )