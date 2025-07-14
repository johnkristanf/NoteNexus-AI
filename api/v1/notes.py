from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from typing import List

from sqlalchemy.orm import Session
from schema.notes import NotesCreate, NotesOut, NotesUpdate
from repository.notes import NotesRepository
from database.init import get_db

router = APIRouter()

@router.post("/new/note", status_code=201)
def create_note(note: NotesCreate, db: Session = Depends(get_db)):
    repo = NotesRepository(db)
    new_note_id = repo.create_note(note)
    return JSONResponse(content={"id": str(new_note_id) }, status_code=201)


@router.get("/fetch/notes", response_model=List[NotesOut])
def get_chat_messages(db: Session = Depends(get_db)):
    repo = NotesRepository(db)
    notes =  repo.get_all_notes()
    return notes 



@router.patch("/note/{note_id}")
def update_note(note_id: int, payload: NotesUpdate, db: Session = Depends(get_db)):
    repo = NotesRepository(db)
    updated_note_id = repo.update_note_content(note_id, payload.updated_content)
    return {"updated_note_id": updated_note_id}



@router.delete("/note/{note_id}")
def update_note(note_id: int, db: Session = Depends(get_db)):
    repo = NotesRepository(db)
    deleted_note_id = repo.delete_note(note_id)
    return {"deleted_note_id": deleted_note_id}