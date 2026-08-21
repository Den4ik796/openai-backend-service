from pydantic import BaseModel
from typing import List
from datetime import datetime

class MessageCreate(BaseModel):
    content: str

class MessageResponse(BaseModel):
    id: int
    role: str
    content: str
    prompt_tokens: int
    completion_tokens: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class SessionResponse(BaseModel):
    id: int
    created_at: datetime
    total_tokens: int
    total_cost: float
    
    class Config:
        from_attributes = True

class SessionDetailResponse(SessionResponse):
    messages: List[MessageResponse]
