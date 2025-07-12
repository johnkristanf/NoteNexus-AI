import tiktoken
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from typing import List
from uuid import UUID

from sqlalchemy.orm import Session
from schema.messages import MessagesCreate, MessagesOut
from repository.messages import MessagesRepository
from database.init import get_db

router = APIRouter()

@router.post("/new/message", status_code=201)
def create_message(message: MessagesCreate, db: Session = Depends(get_db)):
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = encoding.encode(message.content)
    token_count = len(tokens)
    
    repo = MessagesRepository(db)
    message_with_tokens = message.model_copy(update={"token_count": token_count})
    new_message_id = repo.create_message(message_with_tokens)
    
    return JSONResponse(
        status_code=201,
        content={
            "id": str(new_message_id)  # UUID must be converted to string
        }
    )


@router.get("/fetch/messages/{chat_id}", response_model=List[MessagesOut])
def get_chat_messages(chat_id: UUID, db: Session = Depends(get_db)):
    repo = MessagesRepository(db)
    messages =  repo.get_messages_by_chat_id(chat_id)
    return messages 