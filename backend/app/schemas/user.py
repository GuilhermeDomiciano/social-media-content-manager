from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr # Importa BaseModel e EmailStr (para validação de email)

# --- Schemas de Entrada (Request Models) ---

class UserRegister(BaseModel):
    """
    Schema para dados de registro de um novo usuário.
    email: formato de email válido.
    password: deve ser fornecido.
    name: nome do usuário.
    """
    email: EmailStr
    password: str
    name: str

class UserLogin(BaseModel):
    """
    Schema para dados de login do usuário.
    email: email do usuário.
    password: senha do usuário.
    """
    email: EmailStr
    password: str

# --- Schemas de Saída (Response Models) ---

class UserResponse(BaseModel):
    """
    Schema para representar um usuário na resposta da API.
    Não inclui a senha ou hash da senha.
    """
    id: UUID
    email: EmailStr
    name: str
    role: str

    class Config:
        # Permite que o Pydantic mapeie o ID de UUID para str automaticamente
        # e que lide com objetos ORM (SQLModel)
        from_attributes = True # ou 'orm_mode = True' para Pydantic < 2.0

class Token(BaseModel):
    """
    Schema para representar o token de acesso JWT.
    access_token: o token JWT.
    token_type: tipo do token (geralmente "bearer").
    """
    access_token: str
    token_type: str = "bearer"

class ErrorResponse(BaseModel):
    """
    Schema para respostas de erro padronizadas da API.
    code: código do erro (ex: "BAD_REQUEST", "UNAUTHORIZED").
    message: mensagem detalhada do erro (opcional).
    details: lista de objetos com detalhes específicos do erro (opcional).
    """
    code: str
    message: Optional[str] = None
    details: Optional[list[dict]] = None