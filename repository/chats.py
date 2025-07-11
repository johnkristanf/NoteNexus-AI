from sqlalchemy.orm import Session
from models.chats import Chats
from schema.chats import ChatCreate

class ChatsRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def create_chat(self, chat_data: ChatCreate) -> Chats:
        new_chat = Chats(**chat_data.model_dump())
        self.db.add(new_chat)
        self.db.commit()
        self.db.refresh(new_chat)
        return new_chat.id