from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext

# Simulamos una "base de datos" en memoria (luego se reemplaza por una real)
fake_db = {}

# Configuramos el hasher de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

class UserRegister(BaseModel):
    email: EmailStr
    password: str

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

@router.post("/register")
def register_user(user: UserRegister):
    # 1. Verificar si el usuario ya existe
    if user.email in fake_db:
        raise HTTPException(status_code=400, detail="El usuario ya está registrado")

    # 2. Hashear la contraseña
    hashed_pw = hash_password(user.password)

    # 3. Guardar en la base de datos
    fake_db[user.email] = {"email": user.email, "password": hashed_pw}

    return {"message": "Usuario registrado con éxito"}
