"""Configuração de banco de dados do Professor Bang.

O MVP usa SQLite por padrão para facilitar testes locais. Em produção, basta definir
DATABASE_URL com uma URL compatível com SQLAlchemy, por exemplo PostgreSQL.
"""

from __future__ import annotations

import os
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./professor_bang.db")

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """Fornece uma sessão SQLAlchemy por requisição FastAPI."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables() -> None:
    """Cria as tabelas do MVP caso ainda não existam."""
    from app import models  # noqa: F401  # garante registro dos modelos no Base.metadata

    Base.metadata.create_all(bind=engine)
