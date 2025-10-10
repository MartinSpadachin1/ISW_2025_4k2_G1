from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from src.project.workflow.API.login.security import SECRET_KEY, ALGORITHM
router_auth = APIRouter()

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

@router_auth.post("/login")
def login(data: LoginRequest):
    fake_user_db = get_fake_user_db()
    user = fake_user_db.get(data.email)
    if not user or not pwd_context.verify(data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    expiration = datetime.utcnow() + timedelta(hours=1)
    token = jwt.encode({"sub": data.email, "exp": expiration}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}
