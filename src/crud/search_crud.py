from sqlalchemy.orm import Session
from sqlalchemy import or_
from src.models.user_model import User
from src.models.post_model import Post


class SearchCRUD:

    @staticmethod
    def search_users(db: Session, query: str):
        return db.query(User).filter(
            or_(
                User.username.ilike(f"%{query}%"),
                User.full_name.ilike(f"%{query}%"),
                User.email.ilike(f"%{query}%")
            )
        ).all()

    @staticmethod
    def search_posts(db: Session, keyword: str):
        return db.query(Post).filter(
            Post.caption.ilike(f"%{keyword}%")
        ).all()
