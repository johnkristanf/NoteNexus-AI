from pydantic import BaseModel
from datetime import datetime

class NotesCreate(BaseModel):
    user_id: str
    content: str
    
class NotesOut(BaseModel):
    id: int
    content: str
    created_at: datetime
    updated_at: datetime | None 
    
    
class NotesUpdate(BaseModel):
    updated_content: str
    