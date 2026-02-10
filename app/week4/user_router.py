from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.week4.database import get_session
from app.week4.models import User

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.post("/")
def create_user(user: User, session: Session = Depends(get_session)):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@user_router.get("/")
def get_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users


@user_router.get("/{user_id}")
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@user_router.put("/{user_id}")
def update_user(user_id: int, new_data: User, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.username = new_data.username
    user.email = new_data.email
    user.age = new_data.age

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@user_router.delete("/{user_id}")
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    session.delete(user)
    session.commit()

    return {"message": "User deleted"}