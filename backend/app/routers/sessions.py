from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import LearningObservation, StudySession
from app.schemas import ParentDashboard, StudySessionCreate, StudySessionRead

router = APIRouter()


@router.post("", response_model=StudySessionRead)
def create_session(payload: StudySessionCreate, db: Session = Depends(get_db)):
    session = StudySession(**payload.model_dump())
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


@router.get("", response_model=list[StudySessionRead])
def list_sessions(db: Session = Depends(get_db)):
    return db.scalars(select(StudySession).order_by(StudySession.created_at.desc())).all()


@router.get("/parent-dashboard", response_model=ParentDashboard)
def parent_dashboard(db: Session = Depends(get_db)):
    sessions = db.scalars(select(StudySession)).all()
    observations = db.scalars(select(LearningObservation)).all()
    subjects = sorted({session.subject for session in sessions if session.subject})
    total_minutes = sum(session.duration_minutes for session in sessions)
    support_moments = sum(1 for session in sessions if "travada" in session.mode or "apoio" in session.mode)
    strategies = [obs.strategy_that_helped for obs in observations if obs.strategy_that_helped]
    notes = [obs.observation for obs in observations]
    return ParentDashboard(
        studied_subjects=subjects,
        total_study_minutes=total_minutes,
        support_moments=support_moments,
        helpful_strategies=strategies or ["Frases curtas", "Uma pergunta por vez", "Exemplo concreto"],
        weekly_evolution="MVP local: evolução semanal será calculada com mais sessões registradas.",
        pedagogical_notes=notes or ["Observar momentos de travamento e registrar estratégias que ajudaram."],
    )
