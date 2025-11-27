from sqlalchemy.orm import Session
from src.models.follow_model import Follow

class FollowCRUD:

    @staticmethod
    def send_follow_request(db: Session, follower_id: int, following_id: int):
        follow = Follow(
            follower_id=follower_id,
            following_id=following_id
        )
        db.add(follow)
        db.commit()
        db.refresh(follow)
        return follow

    @staticmethod
    def accept_request(db: Session, follow: Follow):
        follow.is_accepted = True
        db.commit()
        return follow

    @staticmethod
    def unfollow(db: Session, follow: Follow):
        db.delete(follow)
        db.commit()
        return True

    @staticmethod
    def get_relation(db: Session, follower_id: int, following_id: int):
        return (
            db.query(Follow)
            .filter(
                Follow.follower_id == follower_id,
                Follow.following_id == following_id,
            )
            .first()
        )