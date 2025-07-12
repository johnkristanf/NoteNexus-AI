from sqlalchemy import select
from sqlalchemy.orm import Session
from models.chats import Chats
from schema.chats import ChatCreate, ChatsOut

class ChatsRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def create_chat(self, chat_data: ChatCreate) -> Chats:
        new_chat = Chats(**chat_data.model_dump())
        self.db.add(new_chat)
        self.db.commit()
        self.db.refresh(new_chat)
        return new_chat.id
    
    def get_all_chats_summary(self) -> list[ChatsOut]:
        stmt = select(Chats.id, Chats.title)
        results = self.db.execute(stmt).all()
        return [{"id": row.id, "title": row.title} for row in results]