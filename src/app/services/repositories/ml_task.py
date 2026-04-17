from typing import List

from sqlmodel import Session, select

from models import MlTask


def get_all_tasks(session: Session) -> List[MlTask]:
    results = session.exec(select(MlTask)).all()
    return list(results)

def get_all_tasks_by_user(user_id:int, session: Session) -> List[MlTask]:
    results = session.exec(select(MlTask).where(MlTask.user_id == user_id)).all()
    return list(results)

def add_task(task: MlTask, session: Session):
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

def merge_task(task: MlTask, session: Session):
    session.merge(task)
    session.commit()
    session.refresh(task)
    return task

def get_task_by_id(task_id:int, session: Session) -> MlTask:
    return session.exec(select(MlTask).where(MlTask.id == task_id)).first()
