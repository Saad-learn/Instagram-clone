from sqlalchemy.orm import Session
from src.models.like_model import Like

class LikeCRUD:

    @staticmethod
    def add_like(db: Session, user_id: int, post_id: int):
        like = Like(user_id=user_id, post_id=post_id)
        db.add(like)
        db.commit()
        db.refresh(like)
        return like

    @staticmethod
    def remove_like(db: Session, like: Like):
        db.delete(like)
        db.commit()
        return True

    @staticmethod
    def get_like(db: Session, user_id: int, post_id: int):
        return (
            db.query(Like)
            .filter(Like.user_id == user_id, Like.post_id == post_id)
            .first()
        )