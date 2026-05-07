from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class StudentProfileBase(BaseModel):
    name: str = Field(..., examples=["Duda"])
    age: int = Field(..., ge=5, le=25)
    difficult_subjects: str = ""
    interests: str = "K-pop, dança, música, idiomas"
    reading_level: str = "iniciante"
    math_level: str = "iniciante"
    anxiety_triggers: str = ""
    helpful_strategies: str = ""


class StudentProfileCreate(StudentProfileBase):
    pass


class StudentProfileRead(StudentProfileBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class StudySessionCreate(BaseModel):
    student_id: int | None = None
    subject: str = "geral"
    mode: str = "me_explica_devagar"
    duration_minutes: int = 0


class StudySessionRead(StudySessionCreate):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class ChatRequest(BaseModel):
    text: str
    mode: str = "me_explica_devagar"
    subject: str = "geral"
    session_id: int | None = None
    repeated_help_requests: int = 0
    recent_errors: int = 0


class PedagogicalStep(BaseModel):
    kind: str
    text: str


class ChatResponse(BaseModel):
    support_mode: bool
    emotional_tone: str
    answer: str
    steps: list[PedagogicalStep]
    question_for_student: str
    hint_options: list[str]
    achievement_suggestion: str | None = None
    safety_note: str | None = None
    raw_json: dict[str, Any]


class RoutineTaskCreate(BaseModel):
    title: str
    order_index: int = 0


class RoutineTaskRead(RoutineTaskCreate):
    id: int
    is_done: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class AchievementCreate(BaseModel):
    title: str
    description: str = ""


class AchievementRead(AchievementCreate):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class ParentDashboard(BaseModel):
    studied_subjects: list[str]
    total_study_minutes: int
    support_moments: int
    helpful_strategies: list[str]
    weekly_evolution: str
    pedagogical_notes: list[str]
