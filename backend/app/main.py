# backend/main.py
#
# Ponto de entrada do Professor Bang — API FastAPI.
#
# Execução a partir de backend/:
#   uvicorn app.main:app --reload --port 8000
#
# Documentação automática:
#   http://localhost:8000/docs  (Swagger UI)
#   http://localhost:8000/redoc (ReDoc)

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.database import create_tables
from app.routes import students, sessions, chat, routine, parents

load_dotenv()


# ─────────────────────────────────────────────────────────────
# Lifespan: cria tabelas na inicialização
# ─────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    print("✅ Banco de dados inicializado.")
    yield
    print("👋 Professor Bang encerrado.")


# ─────────────────────────────────────────────────────────────
# App
# ─────────────────────────────────────────────────────────────

app = FastAPI(
    title="Professor Bang API",
    description=(
        "API do tutor pedagógico adaptativo para adolescentes com "
        "dificuldades de aprendizagem. MVP com motor de IA local."
    ),
    version="1.0.0-mvp",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)


# ─────────────────────────────────────────────────────────────
# CORS — permite Flutter Web e app mobile em desenvolvimento.
# Em produção, defina ALLOWED_ORIGINS com domínios explícitos e não use '*'.
# ─────────────────────────────────────────────────────────────

_default_origins = "http://localhost,http://localhost:3000,http://localhost:5000,http://10.0.2.2:8000"
_allowed_origins = [
    origin.strip()
    for origin in os.getenv("ALLOWED_ORIGINS", _default_origins).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─────────────────────────────────────────────────────────────
# Routers
# ─────────────────────────────────────────────────────────────

app.include_router(students.router)
app.include_router(sessions.router)
app.include_router(chat.router)
app.include_router(routine.router)
app.include_router(parents.router)


# ─────────────────────────────────────────────────────────────
# Health check
# ─────────────────────────────────────────────────────────────

@app.get("/", tags=["Status"])
def root():
    return {
        "app": "Professor Bang",
        "version": "1.0.0-mvp",
        "status": "online",
        "docs": "/docs",
    }


@app.get("/health", tags=["Status"])
def health():
    return {"status": "ok"}
