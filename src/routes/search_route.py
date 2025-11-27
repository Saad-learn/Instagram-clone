from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from src.crud.search_crud import SearchCRUD
from src.schemas.user_schemas import UserOut
from src.schemas.post_schemas import PostOut
from src.database import get_db

router = APIRouter(prefix="/search", tags=["search"])

@router.get("/users", response_model=List[UserOut])
def search_users(q: str, db: Session = Depends(get_db)):
    results = SearchCRUD.search_users(db, query=q)
    return results

@router.get("/posts", response_model=List[PostOut])
def search_posts(q: str, db: Session = Depends(get_db)):
    results = SearchCRUD.search_posts(db, keyword=q)
    return results
