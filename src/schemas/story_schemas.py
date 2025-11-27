from pydantic import BaseModel
from datetime import datetime

class StoryCreate(BaseModel):
    image_url: str

class StoryOut(BaseModel):
    id: int
    image_url: str
    user_id: int
    created_at: datetime
    expires_at: datetime

    class Config:
        from_attributes = True