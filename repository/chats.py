from sqlalchemy import select
from sqlalchemy.orm import Session
from models.chats import Chats
from schema.chats import ChatCreate, ChatsOut
from fastapi import HTTPException, status

class ChatsRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def create_chat(self, chat_data: ChatCreate) -> Chats:
        new_chat = Chats(**chat_data.model_dump())
        self.db.add(new_chat)
        self.db.commit()
        self.db.refresh(new_chat)
        return new_chat.id
    
    def get_all_chats_summary(self, user_id) -> list[ChatsOut]:
        stmt = select(Chats.id, Chats.title).where(Chats.user_id == user_id)
        results = self.db.execute(stmt).all()
        return [{"id": row.id, "title": row.title} for row in results]
    
    
    def update_chat_title(self, chat_id: int, new_title: str) -> Chats:
        chat = self.db.get(Chats, chat_id)
        if not chat:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found")
        chat.title = new_title
        self.db.commit()
        self.db.refresh(chat)
        return chat.id
    
    
    def delete_chat(self, chat_id: int) -> bool:
        chat = self.db.get(Chats, chat_id)
        if not chat:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found")
        self.db.delete(chat)
        self.db.commit()
        return True