import os
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_database_session
from app.models.user import UserModel

SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Configuracion del contexto de cifrado utilizando bcrypt
password_crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Instancia que instruye a FastAPI a buscar el token en la cabecera Authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_crypt_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return password_crypt_context.hash(password)

def create_access_token(subject_identifier: str) -> str:
    expiration_time = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token_payload = {
        "exp": expiration_time,
        "sub": str(subject_identifier)
    }
    encoded_jwt = jwt.encode(token_payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db_session: AsyncSession = Depends(get_database_session)
) -> UserModel:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales de acceso.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
        
    query = select(UserModel).filter(UserModel.username == username)
    result = await db_session.execute(query)
    user = result.scalars().first()
    
    if user is None:
        raise credentials_exception
        
    return user