from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1.chats import router as chats_router
from api.v1.messages import router as messages_router
from api.v1.notes import router as notes_router

# Setup FastAPI app
app = FastAPI()

# Allow CORS for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Your frontend domain
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(chats_router, prefix="/api/v1", tags=["chat"])
app.include_router(messages_router, prefix="/api/v1", tags=["messages"])
app.include_router(notes_router, prefix="/api/v1", tags=["notes"])
