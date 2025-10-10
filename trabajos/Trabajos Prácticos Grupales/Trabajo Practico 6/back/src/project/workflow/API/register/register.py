from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr, Field
from src.project.workflow.API.login.security import hash_password
from sqlmodel import Session
from src.common.persistance.models import Usuario

from src.common.persistance.database import get_session

# Simulamos una "base de datos" en memoria (luego se reemplaza por una real)
fake_db = {}


router = APIRouter()

class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)

'''def hash_password(password: str) -> str:
    return pwd_context.hash(password)'''

@router.post("/register", status_code=201)
def register_user(user: UserRegister,
                  session: Session = Depends(get_session)):
    
    existing_user = session.get(Usuario, user.email)
    # 1. Verificar si el usuario ya existe
    if existing_user:
        raise HTTPException(status_code=400, detail="El mail ya está registrado")

    # 2. Hashear la contraseña
    hashed_pw = hash_password(user.password)

    # 3. Crear el usuario ORM
    new_user = Usuario(email=user.email, hashed_password=hashed_pw)

    # 4. Guardar en la base de datos
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {"message": "Usuario registrado con éxito", "email": new_user.email}
