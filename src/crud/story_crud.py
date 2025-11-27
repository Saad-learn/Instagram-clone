from sqlalchemy.orm import Session
from src.models.story_model import Story
from src.schemas.story_schemas import StoryCreate

class StoryCRUD:

    @staticmethod
    def create_story(db: Session, data: StoryCreate, user_id: int):
        story = Story(
            image_url=data.image_url,
            user_id=user_id
        )
        db.add(story)
        db.commit()
        db.refresh(story)
        return story

    @staticmethod
    def get_story(db: Session, story_id: int):
        return db.query(Story).filter(Story.id == story_id).first()

    @staticmethod
    def delete_story(db: Session, story: Story):
        db.delete(story)
        db.commit()
        return True

    @staticmethod
    def get_user_stories(db: Session, user_id: int):
        return db.query(Story).filter(Story.user_id == user_id).all()

    @staticmethod
    def get_all_stories(db: Session):
        return db.query(Story).all()