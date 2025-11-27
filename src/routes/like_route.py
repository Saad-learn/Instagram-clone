from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.crud.like_crud import LikeCRUD
from src.crud.post_crud import PostCRUD
from src.database import get_db
from src.auth.deps import get_current_user
from src.models.user_model import User as UserModel
from src.models.like_model import Like as LikeModel

router = APIRouter(prefix="/likes", tags=["likes"])

@router.post("/post/{post_id}", response_model=dict)
def like_post(post_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    post = PostCRUD.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    existing = LikeCRUD.get_like(db, user_id=current_user.id, post_id=post_id)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already liked")

    like = LikeCRUD.add_like(db, user_id=current_user.id, post_id=post_id)
    return {"detail": "Liked", "id": like.id}

@router.delete("/post/{post_id}", response_model=dict)
def unlike_post(post_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    like = LikeCRUD.get_like(db, user_id=current_user.id, post_id=post_id)
    if not like:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Like not found")
    LikeCRUD.remove_like(db, like)
    return {"detail": "Unliked"}
