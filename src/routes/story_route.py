from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from src.schemas.story_schemas import StoryCreate, StoryOut
from src.crud.story_crud import StoryCRUD
from src.database import get_db
from src.auth.deps import get_current_user
from src.models.user_model import User as UserModel
from src.models.story_model import Story as StoryModel

router = APIRouter(prefix="/stories", tags=["stories"])

@router.post("/", response_model=StoryOut, status_code=status.HTTP_201_CREATED)
def create_story(payload: StoryCreate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    story = StoryCRUD.create_story(db, payload, user_id=current_user.id)
    return story

@router.get("/{story_id}", response_model=StoryOut)
def get_story(story_id: int, db: Session = Depends(get_db)):
    story = StoryCRUD.get_story(db, story_id)
    if not story:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Story not found")
    return story

@router.delete("/{story_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_story(story_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    story = StoryCRUD.get_story(db, story_id)
    if not story:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Story not found")
    if story.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")
    StoryCRUD.delete_story(db, story)
    return None

@router.get("/user/{user_id}", response_model=List[StoryOut])
def get_user_stories(user_id: int, db: Session = Depends(get_db)):
    stories = StoryCRUD.get_user_stories(db, user_id)
    return stories

@router.get("/", response_model=List[StoryOut])
def get_all_stories(db: Session = Depends(get_db)):
    stories = StoryCRUD.get_all_stories(db)
    return stories
