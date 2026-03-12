from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..models import Task
from ..schemas import TaskCreate
from ..deps import get_db, get_current_user


router = APIRouter()

#CRUD

@router.post("/tasks")
def create_task(task: TaskCreate,
                db: Session = Depends(get_db),
                user=Depends(get_current_user)):

    db_task = Task(
        title=task.title,
        description=task.description,
        owner_id=user.id
    )

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task


@router.get("/tasks")
def get_tasks(db: Session = Depends(get_db),
              user=Depends(get_current_user)):

    return db.query(Task).filter(Task.owner_id == user.id).all()