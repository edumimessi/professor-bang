"""Testes de smoke da API Professor Bang.

Executa o fluxo mínimo do MVP usando FastAPI TestClient:
perfil da aluna → sessão → boas-vindas → mensagem → rotina → conquista → relatório.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

os.environ.setdefault("DATABASE_URL", "sqlite:///./test_professor_bang.db")
os.environ.setdefault("ALLOWED_ORIGINS", "http://localhost")

from fastapi.testclient import TestClient  # noqa: E402

from app.database import Base, engine  # noqa: E402
from app.main import app  # noqa: E402


def reset_database() -> None:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_main_flow() -> None:
    reset_database()
    client = TestClient(app)

    student_payload = {
        "name": "Duda",
        "age": 14,
        "difficult_subjects": ["Matemática", "Português"],
        "interests": ["música", "desenhos", "animais"],
        "reading_level": "medio",
        "math_level": "basico",
        "anxiety_triggers": ["provas", "muita pressão"],
        "helpful_strategies": ["passo a passo", "pausas curtas"],
    }
    student_response = client.post("/students/", json=student_payload)
    assert student_response.status_code == 201, student_response.text
    student = student_response.json()
    assert student["name"] == "Duda"

    session_response = client.post(
        "/sessions/start",
        json={"student_id": student["id"], "subject": "Matemática", "study_mode": "explicacao_guiada"},
    )
    assert session_response.status_code == 201, session_response.text
    session = session_response.json()

    welcome_response = client.post(f"/chat/welcome?session_id={session['id']}")
    assert welcome_response.status_code == 200, welcome_response.text
    assert welcome_response.json()["message"]

    chat_response = client.post(
        "/chat/message",
        json={
            "session_id": session["id"],
            "message": "Não entendi essa conta, estou travada.",
            "subject": "Matemática",
            "study_mode": "explicacao_guiada",
        },
    )
    assert chat_response.status_code == 200, chat_response.text
    chat_data = chat_response.json()
    assert chat_data["message"]
    assert chat_data["is_stuck_detected"] is True

    history_response = client.get(f"/chat/{session['id']}/history")
    assert history_response.status_code == 200, history_response.text
    assert len(history_response.json()) >= 3

    checkin_response = client.post(f"/chat/{session['id']}/checkin?emotion=ansiosa&intensity=4")
    assert checkin_response.status_code == 201, checkin_response.text

    routine_response = client.get(f"/routine/{student['id']}/today")
    assert routine_response.status_code == 200, routine_response.text
    tasks = routine_response.json()
    assert len(tasks) >= 1

    toggle_response = client.put(f"/routine/task/{tasks[0]['id']}/toggle", json={"is_completed": True})
    assert toggle_response.status_code == 200, toggle_response.text
    assert toggle_response.json()["is_completed"] is True

    achievement_response = client.post(
        f"/achievements/{student['id']}?achievement_id=primeiro_passo&title=Primeiro%20passo&description=Começou%20a%20rotina&emoji=estrela"
    )
    assert achievement_response.status_code == 201, achievement_response.text

    end_response = client.put(
        f"/sessions/{session['id']}/end",
        json={"duration_minutes": 15, "notes": "Sessão curta de validação."},
    )
    assert end_response.status_code == 200, end_response.text

    report_response = client.get(f"/parents/{student['id']}/report")
    assert report_response.status_code == 200, report_response.text
    report = report_response.json()
    assert report["student_name"] == "Duda"
    assert report["week_sessions"] >= 1
