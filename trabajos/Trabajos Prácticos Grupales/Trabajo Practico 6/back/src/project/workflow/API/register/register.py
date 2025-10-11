from sqlmodel import select 

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from src.project.workflow.API.login.security import hash_password
from sqlmodel import Session
from src.common.persistance.models import Usuario

from src.common.persistance.database import get_session
from src.common.utils import validar_mail

router = APIRouter()

class UserRegister(BaseModel):
    nombre: str = Field(min_length=1, max_length=50)
    email: str
    password: str = Field(min_length=8, max_length=72)

'''def hash_password(password: str) -> str:
    return pwd_context.hash(password)'''

@router.post("/register", status_code=201)
def register_user(user: UserRegister,
                  session: Session = Depends(get_session)):
    
    # 1. Verificar si el usuario ya existe
    statement = select(Usuario).where(Usuario.email == user.email)
    existing_user = session.exec(statement).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El mail ya está registrado")

    if not validar_mail(user.email):
        raise HTTPException(status_code=400, detail="El mail no es válido")
    # 2. Hashear la contraseña
    hashed_pw = hash_password(user.password)

    # 3. Crear el usuario ORM
    new_user = Usuario(nombre=user.nombre, email=user.email, hashed_password=hashed_pw)

    # 4. Guardar en la base de datos
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {"message": "Usuario registrado con éxito", "email": new_user.email}
