from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import StudentProfile
from app.schemas import StudentProfileCreate, StudentProfileRead

router = APIRouter()


@router.post("", response_model=StudentProfileRead)
def create_profile(payload: StudentProfileCreate, db: Session = Depends(get_db)):
    profile = StudentProfile(**payload.model_dump())
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


@router.get("/{profile_id}", response_model=StudentProfileRead)
def get_profile(profile_id: int, db: Session = Depends(get_db)):
    profile = db.get(StudentProfile, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Perfil não encontrado.")
    return profile


@router.delete("/{profile_id}")
def delete_profile(profile_id: int, db: Session = Depends(get_db)):
    profile = db.get(StudentProfile, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Perfil não encontrado.")
    db.delete(profile)
    db.commit()
    return {"deleted": True, "message": "Perfil removido para respeitar privacidade e controle local."}
