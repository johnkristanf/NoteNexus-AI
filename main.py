from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1.chats import router as chats_router
from api.v1.messages import router as messages_router

# Setup FastAPI app
app = FastAPI()

# Allow CORS for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Your Next.js app origin
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chats_router, prefix="/api/v1", tags=["chat"])
app.include_router(messages_router, prefix="/api/v1", tags=["messages"])
