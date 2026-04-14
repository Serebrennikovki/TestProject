from typing import List
from sqlmodel import Session, select
import hashlib

from models import User


def get_all_users(session: Session) -> List[User]:
    results = session.exec(select(User)).all()
    return list(results)

def get_user_by_id(session: Session, user_id: int) -> User:
    user = session.exec(select(User).where(User.id == user_id)).first()
    return user

def get_user_by_name(session: Session, name: str) -> User:
    user = session.exec(select(User).where(User.name == name)).first()
    if user is None:
        raise Exception(f"нет пользователя с такими именем {name}")
    return user

def create_user(new_user: User, session: Session) -> User:
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user