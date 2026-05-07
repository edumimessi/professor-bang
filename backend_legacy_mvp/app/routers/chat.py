import json

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Message
from app.schemas import ChatRequest, ChatResponse
from app.services.pedagogy import build_pedagogical_response

router = APIRouter()


@router.post("/pedagogical", response_model=ChatResponse)
def pedagogical_chat(payload: ChatRequest, db: Session = Depends(get_db)):
    raw = build_pedagogical_response(payload)

    user_message = Message(
        session_id=payload.session_id,
        role="student",
        content=payload.text,
        structured_json="{}",
    )
    assistant_message = Message(
        session_id=payload.session_id,
        role="assistant",
        content=raw["answer"],
        structured_json=json.dumps(raw, ensure_ascii=False),
    )
    db.add_all([user_message, assistant_message])
    db.commit()

    return ChatResponse(**raw, raw_json=raw)
