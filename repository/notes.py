from typing import List
from sqlalchemy.orm import Session
from models.notes import Notes
from schema.notes import NotesCreate, NotesOut
from fastapi import HTTPException, status

class NotesRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def create_note(self, note_data: NotesCreate) -> Notes:
        new_note = Notes(**note_data.model_dump())
        self.db.add(new_note)
        self.db.commit()
        self.db.refresh(new_note)
        return new_note.id
    
    
    
    def get_all_notes(self, user_id: str) -> List[NotesOut]:
        return (
            self.db.query(Notes)
            .filter(Notes.user_id == user_id)              # ← Add this line
            .order_by(Notes.created_at.desc())
            .all()
        )
        
        
    def update_note_content(self, note_id: int, update_content: str) -> Notes:
        note = self.db.get(Notes, note_id)
        if not note:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
        note.content = update_content
        self.db.commit()
        self.db.refresh(note)
        return note.id
    
    
    def delete_note(self, note_id: int) -> bool:
        note = self.db.get(Notes, note_id)
        if not note:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
        self.db.delete(note)
        self.db.commit()
        return note.id