import os 
import asyncio
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

from fastapi import FastAPI, Request, Query
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware


load_dotenv(dotenv_path="./.env.local")

# Setup FastAPI app
app = FastAPI()

# Allow CORS for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your Next.js app origin
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initalize Chat Model
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
model = ChatOpenAI(model="gpt-4.1-nano", api_key=OPENAI_API_KEY, streaming=True)


# Define Prompt Template
prompt = ChatPromptTemplate([
    ("system",
     "You are Study Mate, a focused AI study assistant specialized in explaining academic theories, concepts, and study materials. "
     "You do **not** generate code, scripts, or programming solutions. "
     "If the user asks for code, politely respond that your role is to assist with theoretical understanding, not programming. "
     "Your answers should be clear, structured, and educational. "
     "Focus on helping students understand ideas, definitions, processes, and real-world applications of knowledge."
    ),
    MessagesPlaceholder(variable_name='history'),
    ("human", "{input}"),
])


# In-memory message history store
store = {}

def get_session_history(session_id: str) -> ChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
        
    # ConversationBufferWindowMemory only get 4 "k" inside the memory
    history = store[session_id]
    while len(history.messages) > 4:
        history.messages.pop(0)
        
    print(f'HISTORY: {history}')
        
    return history


# Create a Conversation Chain
conversational_chain = RunnableWithMessageHistory(
    prompt | model,
    get_session_history,
    input_messages_key='input',
    history_messages_key='history'
)

@app.get('/chat/stream')
async def chat_stream(input: str = Query(...), session_id: str = "default"):
    async def stream_generator():
        try:
            async for chunk in conversational_chain.astream(
                {"input": input},
                config={"configurable": {"session_id": session_id}},
            ):
                yield f"data: {chunk.content}\n\n"
                await asyncio.sleep(0)
            yield "data: [DONE]\n\n"
            
        except Exception as e:
            yield f"data: [ERROR] {str(e)}\n\n"
            
    return StreamingResponse(stream_generator(), status_code=200, media_type="text/event-stream")

