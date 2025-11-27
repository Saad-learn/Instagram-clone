from sqlalchemy.orm import Session
from src.models.user_model import User
from src.schemas.user_schemas import UserCreate
from src.auth.password import hash_password

class UserCRUD:

    @staticmethod
    def create_user(db: Session, data: UserCreate):
        hashed_password = hash_password.hash(data.password)
        user = User(
            username=data.username,
            email=data.email,
            password=hashed_password,
            full_name=data.full_name,
            bio=data.bio,
            profile_picture=data.profile_picture,
            is_private=data.is_private
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_user_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_user_by_id(db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()