from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class StudentProfile(Base):
    __tablename__ = "student_profile"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    difficult_subjects: Mapped[str] = mapped_column(Text, default="")
    interests: Mapped[str] = mapped_column(Text, default="K-pop, dança, música, idiomas")
    reading_level: Mapped[str] = mapped_column(String(80), default="iniciante")
    math_level: Mapped[str] = mapped_column(String(80), default="iniciante")
    anxiety_triggers: Mapped[str] = mapped_column(Text, default="")
    helpful_strategies: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class StudySession(Base):
    __tablename__ = "study_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    student_id: Mapped[int | None] = mapped_column(ForeignKey("student_profile.id"), nullable=True)
    subject: Mapped[str] = mapped_column(String(120), default="geral")
    mode: Mapped[str] = mapped_column(String(120), default="me_explica_devagar")
    duration_minutes: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    messages: Mapped[list["Message"]] = relationship(back_populates="session")


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    session_id: Mapped[int | None] = mapped_column(ForeignKey("study_sessions.id"), nullable=True)
    role: Mapped[str] = mapped_column(String(30), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    structured_json: Mapped[str] = mapped_column(Text, default="{}")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    session: Mapped[StudySession | None] = relationship(back_populates="messages")


class LearningObservation(Base):
    __tablename__ = "learning_observations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    student_id: Mapped[int | None] = mapped_column(ForeignKey("student_profile.id"), nullable=True)
    subject: Mapped[str] = mapped_column(String(120), default="geral")
    observation: Mapped[str] = mapped_column(Text, nullable=False)
    strategy_that_helped: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class EmotionalCheckin(Base):
    __tablename__ = "emotional_checkins"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    student_id: Mapped[int | None] = mapped_column(ForeignKey("student_profile.id"), nullable=True)
    emotion: Mapped[str] = mapped_column(String(80), nullable=False)
    intensity: Mapped[int] = mapped_column(Integer, default=1)
    note: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class RoutineTask(Base):
    __tablename__ = "routine_tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(180), nullable=False)
    is_done: Mapped[bool] = mapped_column(Boolean, default=False)
    order_index: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Achievement(Base):
    __tablename__ = "achievements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(180), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
