from celery import Celery
from datetime import UTC
from sqlalchemy.orm import Session
from src.config import settings
from src.database import SessionLocal
from src.models.story_model import Story

celery_app = Celery(
    "instagram_clone",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,

    task_routes={
        "src.tasks.story_tasks.*": {"queue": "stories"},
    },

    broker_connection_retry_on_startup=True,
    worker_prefetch_multiplier=1,
    task_acks_late=True,
)

@celery_app.task(name="src.tasks.story_tasks.process_story")
def process_story(story_id: int):
    db: Session = SessionLocal()
    try:
        story = db.query(Story).filter(Story.id == story_id).first()
        if story:
            print(f" Story processed: {story.id}")
    finally:
        db.close()

@celery_app.task(name="src.tasks.story_tasks.delete_story_after_24h")
def delete_story_after_24h(story_id: int):
    db: Session = SessionLocal()
    try:
        story = db.query(Story).filter(Story.id == story_id).first()
        if story:
            db.delete(story)
            db.commit()
            print(f" Story auto-deleted: {story.id}")
    finally:
        db.close()
