from pydantic import BaseModel
from typing import Optional
from enums.role import RoleEnum
from uuid import UUID

class MessagesCreate(BaseModel):
    chat_id: UUID
    role: RoleEnum
    content: str
    token_count: Optional[int] = None
