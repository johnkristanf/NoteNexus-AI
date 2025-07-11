from pydantic import BaseModel
from typing import Optional

class ChatCreate(BaseModel):
    title: Optional[str] = None
