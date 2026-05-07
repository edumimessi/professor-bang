"""Schemas Pydantic da API Professor Bang."""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, ConfigDict


class SuccessResponse(BaseModel):
    success: bool = True
    message: str


class StudentProfileBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=120, examples=["Duda"])
    age: int = Field(..., ge=5, le=25, examples=[14])
    difficult_subjects: List[str] = Field(default_factory=list, examples=[["Matemática", "Português"]])
    interests: List[str] = Field(default_factory=list, examples=[["música", "desenhos", "animais"]])
    reading_level: str = Field(default="medio", examples=["medio"])
    math_level: str = Field(default="basico", examples=["basico"])
    anxiety_triggers: List[str] = Field(default_factory=list, examples=[["provas", "muita pressão"]])
    helpful_strategies: List[str] = Field(default_factory=list, examples=[["explicação passo a passo", "pausas curtas"]])


class StudentProfileCreate(StudentProfileBase):
    pass


class StudentProfileUpdate(StudentProfileBase):
    pass


class StudentProfileResponse(StudentProfileBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class StudySessionCreate(BaseModel):
    student_id: int = Field(..., ge=1)
    subject: str = Field(..., min_length=1, max_length=80, examples=["Matemática"])
    study_mode: str = Field(default="explicacao_guiada", max_length=50, examples=["explicacao_guiada"])


class StudySessionEnd(BaseModel):
    duration_minutes: int = Field(..., ge=0, le=600)
    notes: Optional[str] = Field(default=None, max_length=2000)


class StudySessionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    student_id: int
    subject: str
    study_mode: str
    duration_minutes: int
    stuck_count: int
    error_count: int
    notes: Optional[str]
    started_at: datetime
    ended_at: Optional[datetime]


class ChatRequest(BaseModel):
    session_id: int = Field(..., ge=1)
    message: str = Field(..., min_length=1, max_length=4000, examples=["Não entendi essa conta."])
    subject: str = Field(..., min_length=1, max_length=80, examples=["Matemática"])
    study_mode: str = Field(default="explicacao_guiada", max_length=50)


class ChatResponse(BaseModel):
    message: str
    tone: str
    response_type: str
    is_stuck_detected: bool = False
    options: Optional[List[str]] = None
    hint: Optional[str] = None
    next_step: Optional[str] = None
    should_check_in: bool = False


class MessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    session_id: int
    content: str
    is_from_ai: bool
    tone: str
    stuck_detected: bool
    created_at: datetime


class EmotionalCheckinCreate(BaseModel):
    emotion: str = Field(..., min_length=1, max_length=80)
    intensity: int = Field(default=3, ge=1, le=5)


class EmotionalCheckinResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    student_id: int
    session_id: int
    emotion: str
    intensity: int
    created_at: datetime


class RoutineTaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    order_index: int
    is_completed: bool
    completed_at: Optional[datetime]


class RoutineTaskToggle(BaseModel):
    is_completed: bool


class AchievementCreate(BaseModel):
    achievement_id: str = Field(..., min_length=1, max_length=80)
    title: str = Field(..., min_length=1, max_length=160)
    description: str = Field(..., min_length=1, max_length=1000)
    emoji: str = Field(default="⭐", min_length=1, max_length=16)


class AchievementResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    achievement_id: str
    title: str
    description: str
    emoji: str
    earned_at: datetime


class ParentsReport(BaseModel):
    student_name: str
    week_sessions: int
    total_study_minutes: int
    subjects_studied: List[str]
    stuck_moments: int
    recent_achievements: List[AchievementResponse]
    pedagogical_note: str
