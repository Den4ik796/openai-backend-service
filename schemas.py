from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class MessageCreate(BaseModel):
    content: str
    model: Optional[str] = None

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
    id: str
    created_at: datetime
    total_tokens: int
    total_cost: float
    
    class Config:
        from_attributes = True

class SessionDetailResponse(SessionResponse):
    messages: List[MessageResponse]
