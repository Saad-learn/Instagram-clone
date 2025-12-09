from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from src.schemas.comment_schemas import CommentCreate, CommentOut
from src.crud.comment_crud import CommentCRUD
from src.crud.post_crud import PostCRUD
from src.database import get_db
from src.auth.deps import get_current_user
from src.models.user_model import User as UserModel
from src.models.comment_model import Comment as CommentModel

router = APIRouter(prefix="/comments", tags=["comments"])

@router.post("/post/{post_id}", response_model=CommentOut, status_code=status.HTTP_201_CREATED)
def create_comment_for_post(post_id: int, payload: CommentCreate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    post = PostCRUD.get_post(db, post_id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    comment = CommentCRUD.create_comment(db, payload, user_id=current_user.id, post_id=post_id)
    return comment

@router.get("/{comment_id}", response_model=CommentOut)
def get_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = CommentCRUD.get_comment(db, comment_id)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    return comment

@router.put("/{comment_id}", response_model=CommentOut)
def update_comment(comment_id: int, payload: CommentCreate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    comment = CommentCRUD.get_comment(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    post = PostCRUD.get_post(db, comment.post_id)
    if comment.user_id != current_user.id and post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    updated = CommentCRUD.update_comment(db, comment, text=payload.text)
    return updated

@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(comment_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    comment = CommentCRUD.get_comment(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    post = PostCRUD.get_post(db, comment.post_id)
    if comment.user_id != current_user.id and post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    CommentCRUD.delete_comment(db, comment)
    return None

@router.get("/post/{post_id}", response_model=List[CommentOut])
def get_post_comments(post_id: int, db: Session = Depends(get_db)):
    comments = CommentCRUD.get_post_comments(db, post_id)
    return comments

