"""Modelos ORM do MVP Professor Bang."""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


def utc_now() -> datetime:
    """Retorna datetime UTC timezone-aware para campos temporais."""
    return datetime.now(timezone.utc)


class StudentProfile(Base):
    __tablename__ = "student_profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False, index=True)
    age = Column(Integer, nullable=False)
    difficult_subjects = Column(Text, default="")
    interests = Column(Text, default="")
    reading_level = Column(String(30), default="medio")
    math_level = Column(String(30), default="basico")
    anxiety_triggers = Column(Text, default="")
    helpful_strategies = Column(Text, default="")
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)

    sessions = relationship("StudySession", back_populates="student", cascade="all, delete-orphan")
    routine_tasks = relationship("RoutineTask", back_populates="student", cascade="all, delete-orphan")
    achievements = relationship("Achievement", back_populates="student", cascade="all, delete-orphan")
    emotional_checkins = relationship("EmotionalCheckin", back_populates="student", cascade="all, delete-orphan")


class StudySession(Base):
    __tablename__ = "study_sessions"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    subject = Column(String(80), nullable=False, index=True)
    study_mode = Column(String(50), default="explicacao_guiada", nullable=False)
    duration_minutes = Column(Integer, default=0, nullable=False)
    stuck_count = Column(Integer, default=0, nullable=False)
    error_count = Column(Integer, default=0, nullable=False)
    notes = Column(Text, nullable=True)
    started_at = Column(DateTime(timezone=True), default=utc_now, nullable=False, index=True)
    ended_at = Column(DateTime(timezone=True), nullable=True)

    student = relationship("StudentProfile", back_populates="sessions")
    messages = relationship("Message", back_populates="session", cascade="all, delete-orphan")
    emotional_checkins = relationship("EmotionalCheckin", back_populates="session", cascade="all, delete-orphan")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("study_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    content = Column(Text, nullable=False)
    is_from_ai = Column(Boolean, default=False, nullable=False)
    tone = Column(String(50), default="neutro", nullable=False)
    stuck_detected = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False, index=True)

    session = relationship("StudySession", back_populates="messages")


class EmotionalCheckin(Base):
    __tablename__ = "emotional_checkins"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    session_id = Column(Integer, ForeignKey("study_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    emotion = Column(String(80), nullable=False)
    intensity = Column(Integer, default=3, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False, index=True)

    student = relationship("StudentProfile", back_populates="emotional_checkins")
    session = relationship("StudySession", back_populates="emotional_checkins")


class RoutineTask(Base):
    __tablename__ = "routine_tasks"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(180), nullable=False)
    order_index = Column(Integer, default=0, nullable=False)
    is_completed = Column(Boolean, default=False, nullable=False)
    date = Column(DateTime(timezone=True), default=utc_now, nullable=False, index=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    student = relationship("StudentProfile", back_populates="routine_tasks")


class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    achievement_id = Column(String(80), nullable=False, index=True)
    title = Column(String(160), nullable=False)
    description = Column(Text, nullable=False)
    emoji = Column(String(16), default="⭐", nullable=False)
    earned_at = Column(DateTime(timezone=True), default=utc_now, nullable=False, index=True)

    student = relationship("StudentProfile", back_populates="achievements")
