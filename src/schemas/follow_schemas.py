from pydantic import BaseModel
from datetime import datetime

class FollowOut(BaseModel):
    id: int
    follower_id: int
    following_id: int
    is_accepted: bool
    created_at: datetime

    class Config:
        from_attributes = True