from typing import List
from sqlmodel import Session, select
from models import User


def get_all_users(session: Session) -> List[User]:
    results = session.exec(select(User)).all()
    return list(results)

def get_user_by_id(user_id: int, session: Session) -> User:
    user = session.exec(select(User).where(User.id == user_id)).first()
    return user

def get_user_by_login(login: str, session: Session) -> User:
    user = session.exec(select(User).where(User.login == login)).first()
    return user

def create_user(new_user: User, session: Session,) -> User:
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user