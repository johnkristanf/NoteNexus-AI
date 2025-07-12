import asyncio

from fastapi import APIRouter, Body, Depends, Query
from fastapi.responses import StreamingResponse, JSONResponse

from sqlalchemy.orm import Session
from schema.chats import ChatCreate
from repository.chats import ChatsRepository
from chain.conversation import conversational_chain
from database.init import get_db

from schema.chats import ChatsOut
from typing import List

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


@router.get("/fetch/chats", response_model=List[ChatsOut])
def get_chat_messages( db: Session = Depends(get_db)):
    repo = ChatsRepository(db)
    chats = repo.get_all_chats_summary()
    return chats 


@router.post('/send/message')
async def send_llm_message(payload: dict = Body(...)):
    print("ENDITPONT HIT")
    input_text = payload.get("input")
    chat_id = payload.get("chat_id", "default")

    if not input_text:
        return JSONResponse(content={"error": "Missing 'input'"}, status_code=400)

    try:
        response = conversational_chain.invoke(
            {"input": input_text},
            config={"configurable": {"session_id": chat_id}},
        )
        
        print(f'LLM response: {response}')

        # Assuming `response` is an object with `.content` or a dictionary
        return JSONResponse(content={"content": response.content}, status_code=200)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# @router.get('/chat/stream')
# async def chat_stream(input: str = Query(...), chat_id: str = "default"):
#     async def stream_generator():
#         try:
#             async for chunk in conversational_chain.astream(
#                 {"input": input},
#                 config={"configurable": {"session_id": chat_id}},
#             ):
#                 print(f'chunk.content: {chunk.content}')
#                 yield f"data: {chunk.content}\n\n"
#                 await asyncio.sleep(0)
#             yield "data: [DONE]\n\n"
                
#         except Exception as e:
#             yield f"data: [ERROR] {str(e)}\n\n"
    
#     return StreamingResponse(stream_generator(), status_code=200, media_type="text/event-stream")
