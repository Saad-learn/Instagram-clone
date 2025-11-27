from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from src.schemas.user_schemas import UserOut, UserCreate
from src.crud.user_crud import UserCRUD
from src.database import get_db
from src.auth.deps import get_current_user
from src.models.user_model import User as UserModel

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserOut)
def get_me(current_user: UserModel = Depends(get_current_user)):
    return current_user

@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = UserCRUD.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.put("/me", response_model=UserOut)
def update_me(payload: UserCreate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    current_user.username = payload.username
    current_user.email = payload.email
    current_user.full_name = payload.full_name
    current_user.bio = payload.bio
    current_user.profile_picture = payload.profile_picture
    current_user.is_private = payload.is_private

    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user

@router.get("/", response_model=List[UserOut])
def list_users(db: Session = Depends(get_db)):
    users = db.query(UserModel).all()
    return users
