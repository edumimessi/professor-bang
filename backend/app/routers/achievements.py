from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Achievement
from app.schemas import AchievementCreate, AchievementRead

router = APIRouter()

DEFAULT_ACHIEVEMENTS = [
    ("Começou sozinha", "Iniciou uma atividade sem precisar de pressão."),
    ("Tentou mesmo com dificuldade", "Manteve o esforço quando apareceu um desafio."),
    ("Pediu pista", "Usou uma estratégia de autonomia em vez de desistir."),
    ("Terminou uma etapa", "Concluiu uma parte pequena da tarefa."),
    ("Fez pausa e voltou", "Regulou a ansiedade e retomou com calma."),
]


@router.post("/seed", response_model=list[AchievementRead])
def seed_achievements(db: Session = Depends(get_db)):
    existing = db.scalars(select(Achievement)).all()
    if existing:
        return existing
    achievements = [Achievement(title=title, description=description) for title, description in DEFAULT_ACHIEVEMENTS]
    db.add_all(achievements)
    db.commit()
    return db.scalars(select(Achievement).order_by(Achievement.id)).all()


@router.get("", response_model=list[AchievementRead])
def list_achievements(db: Session = Depends(get_db)):
    return db.scalars(select(Achievement).order_by(Achievement.created_at.desc())).all()


@router.post("", response_model=AchievementRead)
def create_achievement(payload: AchievementCreate, db: Session = Depends(get_db)):
    achievement = Achievement(**payload.model_dump())
    db.add(achievement)
    db.commit()
    db.refresh(achievement)
    return achievement
