from fastapi import APIRouter, Depends, HTTPException, status,File, UploadFile
from sqlalchemy.orm import Session
from typing import List
from src.schemas.story_schemas import StoryCreate, StoryOut
from src.crud.story_crud import StoryCRUD
from src.database import get_db
from src.auth.deps import get_current_user
from datetime import UTC, datetime, timedelta
from src.models.user_model import User as UserModel
from src.models.story_model import Story as StoryModel
import cloudinary
from cloudinary.uploader import upload
from src.celery_app import celery_app

router = APIRouter(prefix="/stories", tags=["stories"])

@router.post("/", response_model=StoryOut, status_code=status.HTTP_201_CREATED)
def create_story(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    result = cloudinary.uploader.upload(file.file)
    url = result.get("url")
    expires_at = datetime.now(UTC) + timedelta(hours=24)
    story_data = StoryCreate(
        image_url=url,
        expires_at=expires_at
    )
    story = StoryCRUD.create_story(
        db=db,
        data=story_data,
        user_id=current_user.id
    )
    # celery_app.send_task(
    #     "src.tasks.story_tasks.process_story",
    #     args=[story.id]
    # )
    # celery_app.send_task(
    #     "src.tasks.story_tasks.delete_story_after_24h",
    #     args=[story.id],
    #     countdown=3600
    # )
    from src.celery_app import process_story, delete_story_after_24h

    process_story.delay(story.id)
    delete_story_after_24h.apply_async(args=[story.id], countdown=60)

    return story

@router.get("/{story_id}", response_model=StoryOut)
def get_story(story_id: int, db: Session = Depends(get_db)):
    story = StoryCRUD.get_story(db, story_id)

    if not story:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Story not found")

    if story.expires_at < datetime.utcnow():
        raise HTTPException(status_code=status.HTTP_410_GONE, detail="Story expired")

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
    stories = db.query(StoryModel).filter(
        StoryModel.user_id == user_id,
        StoryModel.expires_at > datetime.utcnow()
    ).all()
    return stories

@router.get("/", response_model=List[StoryOut])
def get_all_stories(db: Session = Depends(get_db)):
    stories = db.query(StoryModel).filter(
        StoryModel.expires_at > datetime.utcnow()
    ).all()
    return stories
