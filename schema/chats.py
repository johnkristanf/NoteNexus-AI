from uuid import UUID
from pydantic import BaseModel
from typing import Optional

class ChatCreate(BaseModel):
    title: Optional[str] = None


class ChatsOut(BaseModel):
    id: UUID
    title: str
    
    
class ChatUpdate(BaseModel):
    title: str