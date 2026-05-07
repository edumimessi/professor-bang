from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.session import Base, engine
from app.routers import achievements, chat, profile, routine, sessions

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Professor Bang API",
    description="API inicial para um sistema pedagógico adaptativo, acolhedor e seguro.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(profile.router, prefix="/api/profile", tags=["Perfil da aluna"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat pedagógico"])
app.include_router(routine.router, prefix="/api/routine", tags=["Rotina de estudo"])
app.include_router(sessions.router, prefix="/api/sessions", tags=["Sessões de estudo"])
app.include_router(achievements.router, prefix="/api/achievements", tags=["Microvitórias"])


@app.get("/")
def root() -> dict[str, str]:
    return {
        "app": "Professor Bang",
        "status": "online",
        "message": "API pedagógica pronta para o MVP local.",
    }
