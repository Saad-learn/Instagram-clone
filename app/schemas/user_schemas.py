from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserCreate(BaseModel):
    username: str= Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str= Field(..., min_length=6)
    display_picture: Optional[str] = None
    is_private: Optional[bool] = False

class UserUpdate(BaseModel):
    username: Optional[str]= Field(..., min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str]= Field(..., min_length=6)
    display_picture: Optional[str] = None
    is_private: Optional[bool] = False

class UserOut(BaseModel):
    id:int
    username:str
    email:EmailStr
    display_picture: Optional[str] = None
    is_private: bool

    class config:
        from_attributes = True
    
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


