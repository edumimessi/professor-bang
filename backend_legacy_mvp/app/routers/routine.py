from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import RoutineTask
from app.schemas import RoutineTaskCreate, RoutineTaskRead

router = APIRouter()

DEFAULT_TASKS = [
    "Pegar caderno",
    "Pegar lápis",
    "Separar água",
    "Abrir tarefa",
    "Estudar por 10 minutos",
    "Fazer pausa",
    "Marcar concluído",
]


@router.post("/seed", response_model=list[RoutineTaskRead])
def seed_routine(db: Session = Depends(get_db)):
    existing = db.scalars(select(RoutineTask)).all()
    if existing:
        return existing
    tasks = [RoutineTask(title=title, order_index=index) for index, title in enumerate(DEFAULT_TASKS)]
    db.add_all(tasks)
    db.commit()
    return db.scalars(select(RoutineTask).order_by(RoutineTask.order_index)).all()


@router.get("", response_model=list[RoutineTaskRead])
def list_tasks(db: Session = Depends(get_db)):
    return db.scalars(select(RoutineTask).order_by(RoutineTask.order_index)).all()


@router.post("", response_model=RoutineTaskRead)
def create_task(payload: RoutineTaskCreate, db: Session = Depends(get_db)):
    task = RoutineTask(**payload.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.patch("/{task_id}/toggle", response_model=RoutineTaskRead)
def toggle_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(RoutineTask, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Tarefa de rotina não encontrada.")
    task.is_done = not task.is_done
    db.commit()
    db.refresh(task)
    return task
