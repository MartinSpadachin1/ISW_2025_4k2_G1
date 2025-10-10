# Archivo: src/project/workflow/API/login/login.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from sqlmodel import Session, select # 💡 Necesario para la DB

from src.project.workflow.API.login.security import SECRET_KEY, ALGORITHM
from src.project.workflow.API.login.security import verify_password
from src.common.persistance.models import Usuario
from src.common.persistance.database import get_session



router_auth = APIRouter(tags=["Auth"])

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def get_fake_user_db():
    """Return a small in-memory user db with hashed password (created at runtime).

    Creating the hash at runtime avoids doing expensive/possibly failing crypto work during module import,
    which can break application startup (uvicorn imports modules on start).
    """
    password = "123"
    hashed = pwd_context.hash(password)
    return {
        "test@example.com": {
            "email": "test@example.com",
            "hashed_password": hashed
        }
    }

class LoginRequest(BaseModel):
    email: str
    password: str

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    
    now = datetime.now(timezone.utc)

    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=15)
    to_encode.update({"exp": expire.timestamp()})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router_auth.post("/login")
def login(data: LoginRequest, 
          session: Session = Depends(get_session)):
    
    statement = select(Usuario).where(Usuario.email == data.email)
    user = session.exec(statement).first()

    if not user:
        raise HTTPException(status_code=400, detail="Email o contraseña incorrectos")
    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Email o contraseña incorrectos")
    
    #Creamos el JWT
    access_token_expires = timedelta(minutes=60)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
