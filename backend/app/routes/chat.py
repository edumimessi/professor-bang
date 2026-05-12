# backend/app/routes/chat.py
#
# Endpoints do chat pedagogico - coracao do Professor Bang.
# Recebe mensagem da aluna, gera resposta via OpenAI quando configurado,
# e usa o motor local como fallback.

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import StudySession, StudentProfile, Message, EmotionalCheckin
from ..schemas import ChatRequest, ChatResponse, MessageResponse
from ..services.ai_pedagogy import pedagogy_engine
from ..services.openai_pedagogy import generate_openai_response

router = APIRouter(prefix="/chat", tags=["Chat Pedagogico"])


def _msg_to_response(m: Message) -> MessageResponse:
    return MessageResponse(
        id=m.id,
        session_id=m.session_id,
        content=m.content,
        is_from_ai=m.is_from_ai,
        tone=m.tone,
        stuck_detected=m.stuck_detected,
        created_at=m.created_at,
    )


def _chat_response(response) -> ChatResponse:
    return ChatResponse(
        message=response.message,
        tone=response.tone,
        response_type=response.response_type,
        is_stuck_detected=response.is_stuck_detected,
        options=response.options,
        hint=response.hint,
        next_step=response.next_step,
        should_check_in=response.should_check_in,
    )


@router.post("/welcome", response_model=ChatResponse)
def get_welcome_message(
    session_id: int,
    db: Session = Depends(get_db),
):
    """Gera e salva a mensagem de boas-vindas ao iniciar sessao."""
    session = db.query(StudySession).filter(StudySession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Sessao nao encontrada.")

    student = db.query(StudentProfile).filter(StudentProfile.id == session.student_id).first()
    interests = [v.strip() for v in (student.interests or "").split(",") if v.strip()]

    response = pedagogy_engine.generate_welcome(
        student_name=student.name,
        subject=session.subject,
        study_mode=session.study_mode,
        interests=interests,
    )

    msg = Message(
        session_id=session_id,
        content=response.message,
        is_from_ai=True,
        tone=response.tone,
        stuck_detected=False,
    )
    db.add(msg)
    db.commit()

    return _chat_response(response)


@router.post("/message", response_model=ChatResponse)
def send_message(data: ChatRequest, db: Session = Depends(get_db)):
    """
    Recebe mensagem da aluna, gera resposta pedagogica e salva ambas.
    Usa OpenAI quando OPENAI_API_KEY estiver configurada; caso contrario,
    usa o motor local de regras.
    """
    session = db.query(StudySession).filter(StudySession.id == data.session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Sessao nao encontrada.")

    student = db.query(StudentProfile).filter(StudentProfile.id == session.student_id).first()
    interests = [v.strip() for v in (student.interests or "").split(",") if v.strip()]

    msg_count = db.query(Message).filter(Message.session_id == data.session_id).count()
    previous_messages = (
        db.query(Message)
        .filter(Message.session_id == data.session_id)
        .order_by(Message.created_at.desc())
        .limit(8)
        .all()
    )
    previous_messages = list(reversed(previous_messages))
    recent_messages = [
        {
            "role": "assistant" if message.is_from_ai else "student",
            "content": message.content,
        }
        for message in previous_messages
    ]

    student_msg = Message(
        session_id=data.session_id,
        content=data.message,
        is_from_ai=False,
        tone="neutro",
        stuck_detected=False,
    )
    db.add(student_msg)

    ai_response = generate_openai_response(
        student_message=data.message,
        study_mode=data.study_mode,
        subject=data.subject,
        student_name=student.name,
        interests=interests,
        reading_level=student.reading_level or "medio",
        message_count=msg_count,
        recent_messages=recent_messages,
    )

    if ai_response is None:
        ai_response = pedagogy_engine.generate_response(
            session_id=data.session_id,
            student_message=data.message,
            study_mode=data.study_mode,
            subject=data.subject,
            student_name=student.name,
            interests=interests,
            reading_level=student.reading_level or "medio",
            message_count=msg_count,
        )

    if ai_response.is_stuck_detected:
        session.stuck_count = (session.stuck_count or 0) + 1

    ai_msg = Message(
        session_id=data.session_id,
        content=ai_response.message,
        is_from_ai=True,
        tone=ai_response.tone,
        stuck_detected=ai_response.is_stuck_detected,
    )
    db.add(ai_msg)
    db.commit()

    return _chat_response(ai_response)


@router.get("/{session_id}/history", response_model=List[MessageResponse])
def get_chat_history(session_id: int, db: Session = Depends(get_db)):
    """Retorna historico completo de mensagens da sessao."""
    messages = (
        db.query(Message)
        .filter(Message.session_id == session_id)
        .order_by(Message.created_at.asc())
        .all()
    )
    return [_msg_to_response(m) for m in messages]


@router.post("/{session_id}/checkin", status_code=201)
def save_emotional_checkin(
    session_id: int,
    emotion: str,
    intensity: int = 3,
    db: Session = Depends(get_db),
):
    """Salva check-in emocional durante a sessao."""
    session = db.query(StudySession).filter(StudySession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Sessao nao encontrada.")

    checkin = EmotionalCheckin(
        student_id=session.student_id,
        session_id=session_id,
        emotion=emotion,
        intensity=max(1, min(5, intensity)),
    )
    db.add(checkin)
    db.commit()
    return {"success": True, "message": "Check-in salvo com carinho"}
