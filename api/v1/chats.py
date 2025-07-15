import asyncio

from fastapi import APIRouter, Body, Depends, Query, UploadFile, Form, File, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse

from sqlalchemy.orm import Session
from schema.chats import ChatCreate, ChatUpdate
from repository.chats import ChatsRepository
from chain.conversation import conversational_chain
from database.init import get_db

from schema.chats import ChatsOut
from typing import List

from docx import Document
import fitz
from io import BytesIO

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
    

@router.patch("/chat/{chat_id}")
def update_chat(chat_id: str, payload: ChatUpdate, db: Session = Depends(get_db)):
    repo = ChatsRepository(db)
    updated_chat_id = repo.update_chat_title(chat_id, payload.title)
    return JSONResponse(content={"updated_chat_id": str(updated_chat_id)}, status_code=200)



@router.delete("/chat/{chat_id}")
def delete_chat(chat_id: str, db: Session = Depends(get_db)):
    repo = ChatsRepository(db)
    repo.delete_chat(chat_id)
    return JSONResponse(content={"message": "Chat deleted successfully"}, status_code=200)



# HANDLE THE LLM RESPONSE LATER EACH FILE TYPE
@router.post("/upload/learning/material")
async def upload_learning_material(    
    chat_id: str = Form(...),
    learningMaterial: UploadFile = File(...)
):
    try:
        if not learningMaterial.filename.endswith(('.pdf', '.doc', '.docx')):
            raise HTTPException(status_code=400, detail="Unsupported file type")
        
        print(f'chat_id: {chat_id}')
        print(f'learningMaterial: {learningMaterial}')

        rawLM = await learningMaterial.read()
        extension = learningMaterial.filename.split('.')[-1].lower()
        content = ""

        if extension == 'docx':
            doc = Document(BytesIO(rawLM))
            content = "\n".join([para.text for para in doc.paragraphs])
            
        elif extension == 'pdf':
            doc = fitz.open(stream=rawLM, filetype="pdf")
            content = "\n".join([page.get_text() for page in doc])

        print(f'Extracted content: {content}')
        if content.strip():  # Check if content is not empty or just whitespace
            input_text = (
                "Extract the **core concepts**, theories, key ideas, and definitions from the following academic material delimited by triple backticks. "
                "At the start of your response, include the Markdown heading: '## 📘 Below are the Key Concepts from your Learning Material'.\n\n"
                "Present the concepts in clean Markdown bullet points. Be concise, avoid summaries, and focus on reusable concepts.\n\n"
                "```\n"
                f"{content}\n"
                "```"
            )
        else:
            input_text = (
                "At the start of your response, include the Markdown heading: '## ⚠️ Unable to Extract Concepts' \n\n"
                "The uploaded material appears to be empty or unreadable. Please check the file and try uploading a different document.\n\n"
                "**Provide a short list of actionable steps in Markdown bullet points that the user can take to resolve this issue.** "
                "The advice should be practical, concise, and relevant to file uploading or readability problems."
            )




        response = conversational_chain.invoke(
            {"input": input_text},
            config={"configurable": {"session_id": chat_id}},  # optional if you're using memory
        )
            
        print(f'response: {response}')
        return JSONResponse(content={"content": response.content})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")




# THIS IS THE ORIGINAL STREAMED RESPONSE CHAT
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
