# backend/app/routes/sessions.py
#
# Endpoints de sessões de estudo.

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone

from ..database import get_db
from ..models import StudySession, StudentProfile
from ..schemas import (
    StudySessionCreate,
    StudySessionEnd,
    StudySessionResponse,
    SuccessResponse,
)

router = APIRouter(prefix="/sessions", tags=["Sessões"])


def _session_to_response(s: StudySession) -> StudySessionResponse:
    return StudySessionResponse(
        id=s.id,
        student_id=s.student_id,
        subject=s.subject,
        study_mode=s.study_mode,
        duration_minutes=s.duration_minutes,
        stuck_count=s.stuck_count,
        error_count=s.error_count,
        notes=s.notes,
        started_at=s.started_at,
        ended_at=s.ended_at,
    )


# ─────────────────────────────────────────────────────────────
# POST /sessions/start
# ─────────────────────────────────────────────────────────────

@router.post("/start", response_model=StudySessionResponse, status_code=201)
def start_session(data: StudySessionCreate, db: Session = Depends(get_db)):
    """Inicia uma nova sessão de estudo."""
    student = db.query(StudentProfile).filter(StudentProfile.id == data.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Aluna não encontrada.")

    session = StudySession(
        student_id=data.student_id,
        subject=data.subject,
        study_mode=data.study_mode,
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return _session_to_response(session)


# ─────────────────────────────────────────────────────────────
# PUT /sessions/{session_id}/end
# ─────────────────────────────────────────────────────────────

@router.put("/{session_id}/end", response_model=StudySessionResponse)
def end_session(session_id: int, data: StudySessionEnd, db: Session = Depends(get_db)):
    """Encerra sessão e salva duração."""
    session = db.query(StudySession).filter(StudySession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Sessão não encontrada.")

    session.ended_at = datetime.now(timezone.utc)
    session.duration_minutes = data.duration_minutes
    if data.notes:
        session.notes = data.notes

    db.commit()
    db.refresh(session)
    return _session_to_response(session)


# ─────────────────────────────────────────────────────────────
# GET /sessions/student/{student_id}
# ─────────────────────────────────────────────────────────────

@router.get("/student/{student_id}", response_model=List[StudySessionResponse])
def list_sessions(student_id: int, limit: int = 20, db: Session = Depends(get_db)):
    """Lista sessões de uma aluna (mais recentes primeiro)."""
    sessions = (
        db.query(StudySession)
        .filter(StudySession.student_id == student_id)
        .order_by(StudySession.started_at.desc())
        .limit(limit)
        .all()
    )
    return [_session_to_response(s) for s in sessions]


# ─────────────────────────────────────────────────────────────
# GET /sessions/{session_id}
# ─────────────────────────────────────────────────────────────

@router.get("/{session_id}", response_model=StudySessionResponse)
def get_session(session_id: int, db: Session = Depends(get_db)):
    """Retorna uma sessão específica."""
    session = db.query(StudySession).filter(StudySession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Sessão não encontrada.")
    return _session_to_response(session)
