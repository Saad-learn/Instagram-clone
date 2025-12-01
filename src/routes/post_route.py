from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session
from typing import List
from src.schemas.post_schemas import PostCreate, PostOut
from src.crud.post_crud import PostCRUD
from src.database import get_db
from src.auth.deps import get_current_user
from src.models.post_model import Post as PostModel
from src.models.user_model import User as UserModel
import cloudinary
from cloudinary.uploader import upload

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_post(caption: str, file: UploadFile = File(...), db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    result = cloudinary.uploader.upload(file.file)
   
    url = result.get("url")
    print(url)
    post = PostCRUD.create_post(db, caption, user_id=current_user.id, url=url)
    return post

@router.get("/{post_id}", response_model=PostOut)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = PostCRUD.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    # print(post.images)
    db.refresh(post, attribute_names=["images"])

    return post

@router.put("/{post_id}", response_model=PostOut)
def update_post(post_id: int, payload: PostCreate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    post = PostCRUD.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")
    updated = PostCRUD.update_post(db, post, caption=payload.caption)
    return updated

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    post = PostCRUD.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")
    PostCRUD.delete_post(db, post)
    return None

@router.get("/user/{user_id}", response_model=List[PostOut])
def list_user_posts(user_id: int, db: Session = Depends(get_db)):
    posts = PostCRUD.list_user_posts(db, user_id)
    return posts
