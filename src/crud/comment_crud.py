from sqlalchemy.orm import Session
from src.models.comment_model import Comment
from src.schemas.comment_schemas import CommentCreate

class CommentCRUD:

    @staticmethod
    def create_comment(db: Session, data: CommentCreate, user_id: int, post_id: int):
        comment = Comment(
            text=data.text,
            user_id=user_id,
            post_id=post_id
        )
        db.add(comment)
        db.commit()
        db.refresh(comment)
        return comment

    @staticmethod
    def get_comment(db: Session, comment_id: int):
        return db.query(Comment).filter(Comment.id == comment_id).first()

    @staticmethod
    def update_comment(db: Session, comment: Comment, text: str):
        comment.text = text
        db.commit()
        db.refresh(comment)
        return comment

    @staticmethod
    def delete_comment(db: Session, comment: Comment):
        db.delete(comment)
        db.commit()
        return True

    @staticmethod
    def get_post_comments(db: Session, post_id: int):
        return db.query(Comment).filter(Comment.post_id == post_id).all()