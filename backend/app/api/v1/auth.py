from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.core.config import get_settings
from app.core.database import get_session
from app.core.security import create_access_token # type: ignore
from app.services.user_service import register_user, authenticate_user # type: ignore
from app.schemas.user import UserRegister, UserLogin, UserResponse, Token, ErrorResponse

settings = get_settings()

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse, "description": "Bad Request"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse, "description": "Server Error"},
    },
)
async def register(
    user_data: UserRegister,
    db: Annotated[Session, Depends(get_session)]
):
    """
    Endpoint para registrar um novo usuário.
    """
    try:
        new_user = await register_user(user_data, db)
        return new_user
    except HTTPException as e:
        raise e # Relança as exceções HTTP com seus detalhes
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": "SERVER_ERROR", "message": str(e)}
        )

@router.post(
    "/login",
    response_model=Token,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponse, "description": "Unauthorized"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse, "description": "Server Error"},
    },
)
async def login(
    user_data: UserLogin,
    db: Annotated[Session, Depends(get_session)]
):
    """
    Endpoint para login de usuário. Retorna um token JWT.
    """
    try:
        auth_result = await authenticate_user(user_data, db)
        access_token = auth_result["access_token"]
        # user_id = auth_result["user_id"] # Se precisar usar o ID do usuário para criar um token interno

        # Para este MVP, estamos usando o token diretamente do Supabase.
        # Se você fosse gerar seu próprio token, seria assim:
        # access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        # access_token = create_access_token(
        #     data={"sub": user_id}, expires_delta=access_token_expires
        # )

        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException as e:
        raise e # Relança as exceções HTTP com seus detalhes
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": "SERVER_ERROR", "message": str(e)}
        )