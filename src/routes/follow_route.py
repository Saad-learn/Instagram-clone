from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.crud.follow_crud import FollowCRUD
from src.crud.user_crud import UserCRUD
from src.database import get_db
from src.auth.deps import get_current_user
from src.models.follow_model import Follow as FollowModel
from src.models.user_model import User as UserModel

router = APIRouter(prefix="/follows", tags=["follows"])

@router.post("/request/{target_user_id}", response_model=dict)
def send_follow_request(target_user_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    if target_user_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot follow yourself")

    target = UserCRUD.get_user_by_id(db, target_user_id)
    if not target:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Target user not found")

    existing = FollowCRUD.get_relation(db, follower_id=current_user.id, following_id=target_user_id)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Follow relation already exists")

    follow = FollowCRUD.send_follow_request(db, follower_id=current_user.id, following_id=target_user_id)
    return {"detail": "Follow request sent", "id": follow.id}

@router.post("/accept/{follow_id}", response_model=dict)
def accept_follow(follow_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    follow = db.query(FollowModel).filter(FollowModel.id == follow_id).first()
    if not follow:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Follow request not found")
    if follow.following_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")

    updated = FollowCRUD.accept_request(db, follow)
    return {"detail": "Follow accepted", "id": updated.id}

@router.delete("/unfollow/{follow_id}", response_model=dict)
def unfollow(follow_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    follow = db.query(FollowModel).filter(FollowModel.id == follow_id).first()
    if not follow:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Follow not found")
    if follow.follower_id != current_user.id and follow.following_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")
    FollowCRUD.unfollow(db, follow)
    return {"detail": "Unfollowed"}
