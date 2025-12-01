from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class PostCreate(BaseModel):
    caption: Optional[str] = None

class PostImageOut(BaseModel):
    id: int
    image_url: str
    
    class Config:
        from_attributes = True

class PostOut(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    images: List[PostImageOut]

    class Config:
        from_attributes = True

