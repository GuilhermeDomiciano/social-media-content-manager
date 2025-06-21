import httpx
from uuid import UUID
from sqlmodel import Session, select
from fastapi import HTTPException, status
from typing import Optional

from app.core.config import get_settings
from app.models.user import User
from app.schemas.user import UserRegister, UserLogin
# from app.core.security import get_password_hash, verify_password # Se estivesse usando auth interno

settings = get_settings()

async def register_user(user_data: UserRegister, db: Session) -> User:
    """
    Registra um novo usuário no Supabase Auth e na tabela 'users' do DB.
    """
    # URLs da API Supabase Auth
    supabase_auth_url = f"{settings.SUPABASE_URL}/auth/v1/signup" # Ajustar para a URL real do Supabase

    # O Supabase Auth lida com o hashing da senha internamente
    auth_payload = {
        "email": user_data.email,
        "password": user_data.password,
        "options": {
            "data": {
                "full_name": user_data.name # Exemplo de metadados para o Supabase Auth
            }
        }
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                supabase_auth_url,
                json=auth_payload,
                headers={
                    "apikey": settings.SUPABASE_KEY,
                    "Content-Type": "application/json"
                }
            )
            response.raise_for_status() # Levanta exceção para erros HTTP (4xx ou 5xx)

            supabase_user_data = response.json()
            # O ID do usuário retornado pelo Supabase Auth
            user_id_from_supabase = supabase_user_data["user"]["id"]

            # Criar o registro do usuário na sua tabela 'users'
            # Assumimos que o ID do usuário Supabase é o mesmo que o PK na nossa tabela 'users'
            new_user = User(
                id=UUID(user_id_from_supabase),
                email=user_data.email,
                name=user_data.name,
                role="user" # Papel padrão para novos usuários
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user) # Atualiza o objeto new_user com os dados do DB (ex: created_at)
            return new_user

        except httpx.HTTPStatusError as e:
            # Tratar erros específicos do Supabase Auth
            if e.response.status_code == 400:
                error_detail = e.response.json().get("msg", "Bad request to Supabase Auth.")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={"code": "BAD_REQUEST", "message": f"Erro no Supabase Auth: {error_detail}"}
                )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"code": "SERVER_ERROR", "message": f"Falha ao registrar usuário no Supabase: {e.response.text}"}
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"code": "SERVER_ERROR", "message": f"Erro inesperado ao registrar usuário: {str(e)}"}
            )

async def authenticate_user(user_data: UserLogin, db: Session) -> dict:
    """
    Autentica um usuário contra o Supabase Auth e retorna o token de acesso.
    Retorna um dicionário contendo 'access_token' e 'user_id'.
    """
    # URL da API Supabase Auth para sign-in
    supabase_auth_url = f"{settings.SUPABASE_URL}/auth/v1/token?grant_type=password"

    auth_payload = {
        "email": user_data.email,
        "password": user_data.password
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                supabase_auth_url,
                json=auth_payload,
                headers={
                    "apikey": settings.SUPABASE_KEY,
                    "Content-Type": "application/json"
                }
            )
            response.raise_for_status() # Levanta exceção para erros HTTP

            supabase_response_data = response.json()
            access_token = supabase_response_data["access_token"]
            user_id = supabase_response_data["user"]["id"] # O ID do usuário do Supabase Auth

            return {"access_token": access_token, "user_id": user_id}

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 400: # Supabase retorna 400 para credenciais inválidas
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail={"code": "UNAUTHORIZED", "message": "Credenciais inválidas."}
                )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"code": "SERVER_ERROR", "message": f"Falha ao autenticar no Supabase: {e.response.text}"}
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"code": "SERVER_ERROR", "message": f"Erro inesperado ao autenticar usuário: {str(e)}"}
            )

# Função para obter um usuário do DB (útil para get_current_user no security.py)
def get_user_by_id(user_id: UUID, db: Session) -> Optional[User]:
    """
    Busca um usuário na tabela 'users' pelo seu ID.
    """
    statement = select(User).where(User.id == user_id)
    user = db.exec(statement).first()
    return user