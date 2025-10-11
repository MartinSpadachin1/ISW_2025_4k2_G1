from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
from passlib.context import CryptContext
from src.project.workflow.API.config import SECRET_KEY, ALGORITHM

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

security = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si una contraseña en texto plano coincide con el hash almacenado.
    
    Args:
        plain_password (str): La contraseña ingresada por el usuario.
        hashed_password (str): El hash de la contraseña almacenado en la DB (user.password_hash).
        
    Returns:
        bool: True si coinciden, False en caso contrario.
    """
    # Truncar la contraseña de entrada si es demasiado larga, al igual que en hash_password, 
    # para evitar el ValueError: password cannot be longer than 72 bytes.
    truncated_password = plain_password.encode('utf-8')[:72]
    
    # pwd_context.verify() es el método clave que maneja la lógica de comparación
    return pwd_context.verify(truncated_password, hashed_password)

def hash_password(password: str) -> str:
    """
    Genera el hash de una contraseña, TRUNCANDO la entrada a 72 bytes,
    ya que bcrypt tiene esta limitación.
    """
    # La línea clave: Truncar la contraseña codificada a 72 bytes.
    truncated_password = password.encode('utf-8')[:72]
    
    # Llama a .hash() con la contraseña TRUNCADA
    return pwd_context.hash(truncated_password)


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except:
        raise HTTPException(status_code=401, detail="Token inválido")