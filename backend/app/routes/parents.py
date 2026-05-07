# backend/app/routes/parents.py
#
# Endpoint do painel dos responsáveis.
# Gera relatório semanal com dados pedagógicos (sem exposição de conteúdo do chat).

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta

from ..database import get_db
from ..models import StudentProfile, StudySession, Achievement
from ..schemas import ParentsReport, AchievementResponse
from ..services.ai_pedagogy import pedagogy_engine

router = APIRouter(prefix="/parents", tags=["Painel dos Responsáveis"])


@router.get("/{student_id}/report", response_model=ParentsReport)
def get_parents_report(student_id: int, db: Session = Depends(get_db)):
    """
    Retorna relatório semanal para os responsáveis.
    Inclui: sessões, minutos de estudo, matérias, momentos de dificuldade,
    conquistas recentes e nota pedagógica gerada automaticamente.
    """
    student = db.query(StudentProfile).filter(StudentProfile.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Aluna não encontrada.")

    # Janela: últimos 7 dias
    week_ago = datetime.now(timezone.utc) - timedelta(days=7)

    sessions = (
        db.query(StudySession)
        .filter(
            StudySession.student_id == student_id,
            StudySession.started_at >= week_ago,
        )
        .all()
    )

    week_sessions = len(sessions)
    total_minutes = sum(s.duration_minutes or 0 for s in sessions)
    stuck_moments = sum(s.stuck_count or 0 for s in sessions)

    subjects = list({s.subject for s in sessions if s.subject})

    # Conquistas recentes (última semana)
    recent_achievements = (
        db.query(Achievement)
        .filter(
            Achievement.student_id == student_id,
            Achievement.earned_at >= week_ago,
        )
        .order_by(Achievement.earned_at.desc())
        .limit(5)
        .all()
    )

    achievements_resp = [
        AchievementResponse(
            id=a.id,
            achievement_id=a.achievement_id,
            title=a.title,
            description=a.description,
            emoji=a.emoji,
            earned_at=a.earned_at,
        )
        for a in recent_achievements
    ]

    # Nota pedagógica automática
    note = pedagogy_engine.generate_pedagogical_note(
        week_sessions=week_sessions,
        stuck_moments=stuck_moments,
        subjects=subjects,
    )

    return ParentsReport(
        student_name=student.name,
        week_sessions=week_sessions,
        total_study_minutes=total_minutes,
        subjects_studied=subjects,
        stuck_moments=stuck_moments,
        recent_achievements=achievements_resp,
        pedagogical_note=note,
    )
