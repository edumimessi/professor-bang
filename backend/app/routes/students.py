# backend/app/routes/students.py
#
# Endpoints de gerenciamento do perfil pedagógico da aluna.

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import StudentProfile
from ..schemas import (
    StudentProfileCreate,
    StudentProfileUpdate,
    StudentProfileResponse,
    SuccessResponse,
)

router = APIRouter(prefix="/students", tags=["Aluna"])


def _csv_to_list(value: str) -> List[str]:
    """Converte string CSV → lista (ex: 'A,B,C' → ['A','B','C'])."""
    return [v.strip() for v in value.split(",") if v.strip()] if value else []


def _list_to_csv(lst: List[str]) -> str:
    """Converte lista → CSV."""
    return ",".join(lst)


def _profile_to_response(profile: StudentProfile) -> StudentProfileResponse:
    """Converte modelo ORM → schema de resposta, expandindo CSV."""
    return StudentProfileResponse(
        id=profile.id,
        name=profile.name,
        age=profile.age,
        difficult_subjects=_csv_to_list(profile.difficult_subjects or ""),
        interests=_csv_to_list(profile.interests or ""),
        reading_level=profile.reading_level,
        math_level=profile.math_level,
        anxiety_triggers=_csv_to_list(profile.anxiety_triggers or ""),
        helpful_strategies=_csv_to_list(profile.helpful_strategies or ""),
        created_at=profile.created_at,
        updated_at=profile.updated_at,
    )


# ─────────────────────────────────────────────────────────────
# GET /students/
# ─────────────────────────────────────────────────────────────

@router.get("/", response_model=List[StudentProfileResponse])
def list_students(db: Session = Depends(get_db)):
    """Lista todos os perfis cadastrados."""
    profiles = db.query(StudentProfile).all()
    return [_profile_to_response(p) for p in profiles]


# ─────────────────────────────────────────────────────────────
# POST /students/
# ─────────────────────────────────────────────────────────────

@router.post("/", response_model=StudentProfileResponse, status_code=status.HTTP_201_CREATED)
def create_student(data: StudentProfileCreate, db: Session = Depends(get_db)):
    """Cria um novo perfil pedagógico."""
    profile = StudentProfile(
        name=data.name,
        age=data.age,
        difficult_subjects=_list_to_csv(data.difficult_subjects),
        interests=_list_to_csv(data.interests),
        reading_level=data.reading_level,
        math_level=data.math_level,
        anxiety_triggers=_list_to_csv(data.anxiety_triggers),
        helpful_strategies=_list_to_csv(data.helpful_strategies),
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return _profile_to_response(profile)


# ─────────────────────────────────────────────────────────────
# GET /students/{student_id}
# ─────────────────────────────────────────────────────────────

@router.get("/{student_id}", response_model=StudentProfileResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    """Retorna perfil por ID."""
    profile = db.query(StudentProfile).filter(StudentProfile.id == student_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Perfil não encontrado.")
    return _profile_to_response(profile)


# ─────────────────────────────────────────────────────────────
# PUT /students/{student_id}
# ─────────────────────────────────────────────────────────────

@router.put("/{student_id}", response_model=StudentProfileResponse)
def update_student(
    student_id: int,
    data: StudentProfileUpdate,
    db: Session = Depends(get_db),
):
    """Atualiza perfil existente."""
    profile = db.query(StudentProfile).filter(StudentProfile.id == student_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Perfil não encontrado.")

    profile.name = data.name
    profile.age = data.age
    profile.difficult_subjects = _list_to_csv(data.difficult_subjects)
    profile.interests = _list_to_csv(data.interests)
    profile.reading_level = data.reading_level
    profile.math_level = data.math_level
    profile.anxiety_triggers = _list_to_csv(data.anxiety_triggers)
    profile.helpful_strategies = _list_to_csv(data.helpful_strategies)

    db.commit()
    db.refresh(profile)
    return _profile_to_response(profile)


# ─────────────────────────────────────────────────────────────
# DELETE /students/{student_id}  — LGPD: apaga todos os dados
# ─────────────────────────────────────────────────────────────

@router.delete("/{student_id}", response_model=SuccessResponse)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    """
    Remove perfil e TODOS os dados associados (LGPD — direito ao esquecimento).
    Irreversível.
    """
    profile = db.query(StudentProfile).filter(StudentProfile.id == student_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Perfil não encontrado.")

    db.delete(profile)
    db.commit()
    return SuccessResponse(message="Todos os dados da aluna foram removidos permanentemente.")
