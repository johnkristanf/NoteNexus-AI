import asyncio

from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse, JSONResponse

from sqlalchemy.orm import Session
from schema.chats import ChatCreate
from repository.chats import ChatsRepository
from chain.conversation import conversational_chain
from database.init import get_db

router = APIRouter()

@router.post("/new/chat", status_code=201)
def create_chat(chat: ChatCreate, db: Session = Depends(get_db)):
    repo = ChatsRepository(db)
    new_chat_id = repo.create_chat(chat)
    return JSONResponse(
        status_code=201,
        content={
            "id": str(new_chat_id)  # UUID must be converted to string
        }
    )


@router.get('/chat/stream')
async def chat_stream(input: str = Query(...), chat_id: str = "default",  db: Session = Depends(get_db), ):
    async def stream_generator():
        try:
            async for chunk in conversational_chain.astream(
                {"input": input},
                config={"configurable": {"session_id": chat_id}},
            ):
                print(f'chunk.content: {chunk.content}')
                yield f"data: {chunk.content}\n\n"
                await asyncio.sleep(0)
            yield "data: [DONE]\n\n"
                
        except Exception as e:
            yield f"data: [ERROR] {str(e)}\n\n"
    
    return StreamingResponse(stream_generator(), status_code=200, media_type="text/event-stream")
