from sqlalchemy.orm import Session
from src.models.post_model import Post, PostImage
from src.schemas.post_schemas import PostCreate

class PostCRUD:

    @staticmethod
    def create_post(db: Session, caption: str, user_id: int, url: str):
        post = Post(
            caption=caption,
            user_id=user_id
        )
        db.add(post)
        db.commit()
        db.refresh(post)
        url
        return post

    @staticmethod
    def get_post(db: Session, post_id: int):
        return db.query(Post).filter(Post.id == post_id).first()

    @staticmethod
    def update_post(db: Session, post: Post, caption: str):
        post.caption = caption
        db.commit()
        db.refresh(post)
        return post

    @staticmethod
    def delete_post(db: Session, post: Post):
        db.delete(post)
        db.commit()
        return True

    @staticmethod
    def list_user_posts(db: Session, user_id: int):
        return db.query(Post).filter(Post.user_id == user_id).all()