from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from app.core.config import get_settings # Importar as configurações

# Contexto para hashing de senhas
# O esquema 'bcrypt' é recomendado para segurança
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se uma senha em texto puro corresponde a uma senha hasheada.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Gera o hash de uma senha em texto puro.
    """
    return pwd_context.hash(password)

settings = get_settings()

# O tokenUrl deve corresponder ao endpoint de login da sua API
# Ele é usado pelo FastAPI para gerar a documentação OpenAPI/Swagger UI
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Cria um token de acesso JWT.
    data: Dicionário com os dados a serem incluídos no token (ex: {"sub": user_id})
    expires_delta: Opcional, tempo de expiração do token. Se None, usa um padrão.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # Padrão: token expira em 30 minutos
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> dict:
    """
    Decodifica um token JWT e retorna os dados contidos nele.
    Levanta HTTPException se o token for inválido ou expirado.
    """
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
        # Aqui você pode adicionar validações adicionais ao payload, se necessário
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
# Continuar no arquivo app/core/security.py

# Para este exemplo, get_current_user irá apenas retornar o 'sub' (subject, que será o user_id)
# Em um passo futuro, ela poderá buscar o objeto User completo do banco de dados.
def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    """
    Retorna o ID do usuário autenticado a partir do token JWT.
    Levanta HTTPException se o token for inválido ou ausente.
    """
    payload = decode_token(token)
    user_id: str = payload.get("sub") # 'sub' é uma convenção para o subject (identificador do usuário)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Por enquanto, retornamos o ID do usuário.
    # No futuro, aqui você poderia buscar o usuário no DB para retornar um objeto User completo.
    return user_id