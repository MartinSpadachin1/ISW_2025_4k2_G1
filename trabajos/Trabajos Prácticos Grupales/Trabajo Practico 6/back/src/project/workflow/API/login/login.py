# Archivo: src/project/workflow/API/login/login.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from sqlmodel import Session, select 

from src.project.workflow.API.config import SECRET_KEY, ALGORITHM
from src.project.workflow.API.login.security import verify_password
from src.common.persistance.models import Usuario
from src.common.persistance.database import get_session



router_auth = APIRouter(tags=["Auth"])

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")



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
