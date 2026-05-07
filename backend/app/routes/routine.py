# backend/app/routes/routine.py
#
# Endpoints de rotina diária e conquistas.

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone, date, timedelta

from ..database import get_db
from ..models import RoutineTask, StudentProfile, Achievement
from ..schemas import (
    RoutineTaskResponse,
    RoutineTaskToggle,
    AchievementResponse,
    SuccessResponse,
)

router = APIRouter(tags=["Rotina e Conquistas"])

# ─────────── Tarefas padrão ───────────────────────────────────

DEFAULT_TASKS = [
    "☀️ Acordei e tomei café",
    "🎒 Separei o material escolar",
    "📖 Li por 10 minutinhos",
    "✏️ Fiz minha lição de casa",
    "🧘 Pausa de respiração",
    "🌙 Revisei o que aprendi hoje",
]


def _task_to_response(t: RoutineTask) -> RoutineTaskResponse:
    return RoutineTaskResponse(
        id=t.id,
        title=t.title,
        order_index=t.order_index,
        is_completed=t.is_completed,
        completed_at=t.completed_at,
    )


def _achievement_to_response(a: Achievement) -> AchievementResponse:
    return AchievementResponse(
        id=a.id,
        achievement_id=a.achievement_id,
        title=a.title,
        description=a.description,
        emoji=a.emoji,
        earned_at=a.earned_at,
    )


# ─────────────────────────────────────────────────────────────
# GET /routine/{student_id}/today
# ─────────────────────────────────────────────────────────────

@router.get("/routine/{student_id}/today", response_model=List[RoutineTaskResponse])
def get_today_routine(student_id: int, db: Session = Depends(get_db)):
    """
    Retorna as tarefas de hoje. Cria automaticamente se não existirem.
    """
    student = db.query(StudentProfile).filter(StudentProfile.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Aluna não encontrada.")

    today_start = datetime.combine(date.today(), datetime.min.time()).replace(tzinfo=timezone.utc)
    today_end = today_start + timedelta(days=1)

    tasks = (
        db.query(RoutineTask)
        .filter(
            RoutineTask.student_id == student_id,
            RoutineTask.date >= today_start,
            RoutineTask.date < today_end,
        )
        .order_by(RoutineTask.order_index)
        .all()
    )

    # Cria tarefas padrão se não existirem para hoje
    if not tasks:
        for i, title in enumerate(DEFAULT_TASKS):
            task = RoutineTask(
                student_id=student_id,
                title=title,
                order_index=i,
                is_completed=False,
                date=today_start,
            )
            db.add(task)
        db.commit()

        tasks = (
            db.query(RoutineTask)
            .filter(
                RoutineTask.student_id == student_id,
                RoutineTask.date >= today_start,
                RoutineTask.date < today_end,
            )
            .order_by(RoutineTask.order_index)
            .all()
        )

    return [_task_to_response(t) for t in tasks]


# ─────────────────────────────────────────────────────────────
# PUT /routine/task/{task_id}/toggle
# ─────────────────────────────────────────────────────────────

@router.put("/routine/task/{task_id}/toggle", response_model=RoutineTaskResponse)
def toggle_task(task_id: int, data: RoutineTaskToggle, db: Session = Depends(get_db)):
    """Marca ou desmarca uma tarefa como concluída."""
    task = db.query(RoutineTask).filter(RoutineTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada.")

    task.is_completed = data.is_completed
    task.completed_at = datetime.now(timezone.utc) if data.is_completed else None

    db.commit()
    db.refresh(task)
    return _task_to_response(task)


# ─────────────────────────────────────────────────────────────
# CONQUISTAS
# ─────────────────────────────────────────────────────────────

@router.get("/achievements/{student_id}", response_model=List[AchievementResponse])
def list_achievements(student_id: int, db: Session = Depends(get_db)):
    """Lista todas as conquistas da aluna."""
    achievements = (
        db.query(Achievement)
        .filter(Achievement.student_id == student_id)
        .order_by(Achievement.earned_at.desc())
        .all()
    )
    return [_achievement_to_response(a) for a in achievements]


@router.post("/achievements/{student_id}", response_model=AchievementResponse, status_code=201)
def unlock_achievement(
    student_id: int,
    achievement_id: str,
    title: str,
    description: str,
    emoji: str,
    db: Session = Depends(get_db),
):
    """
    Desbloqueia uma conquista para a aluna.
    Ignora se já desbloqueada (idempotente).
    """
    existing = (
        db.query(Achievement)
        .filter(
            Achievement.student_id == student_id,
            Achievement.achievement_id == achievement_id,
        )
        .first()
    )
    if existing:
        return _achievement_to_response(existing)

    achievement = Achievement(
        student_id=student_id,
        achievement_id=achievement_id,
        title=title,
        description=description,
        emoji=emoji,
    )
    db.add(achievement)
    db.commit()
    db.refresh(achievement)
    return _achievement_to_response(achievement)
