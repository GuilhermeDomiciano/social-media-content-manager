from typing import Annotated # Para usar Annotated para dependências
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.core.database import get_session # type: ignore
from app.core.security import get_current_user # type: ignore # Importa a dependência de segurança
from app.services.user_service import get_user_by_id # type: ignore # Importa o serviço para buscar o usuário
from app.schemas.user import UserResponse, ErrorResponse # Importa o schema de resposta para usuário

router = APIRouter(prefix="/users", tags=["Users"])

@router.get(
    "/me",
    response_model=UserResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponse, "description": "Unauthorized"},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse, "description": "User not found"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse, "description": "Server Error"},
    },
)
def read_users_me(
    current_user_id: Annotated[UUID, Depends(get_current_user)], # Injeta o ID do usuário autenticado
    db: Annotated[Session, Depends(get_session)] # Injeta a sessão do banco de dados
):
    """
    Retorna informações sobre o usuário autenticado.
    Requer um token JWT válido no cabeçalho Authorization (Bearer token).
    """
    user = get_user_by_id(current_user_id, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "NOT_FOUND", "message": "Usuário não encontrado."}
        )
    return user