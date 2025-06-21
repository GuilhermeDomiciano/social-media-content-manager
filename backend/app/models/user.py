from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime

from sqlmodel import Field, SQLModel # Importa Field e SQLModel

# Define o modelo SQLModel para a tabela 'users'
class User(SQLModel, table=True):
    """
    Representa um usuário no banco de dados.
    """
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True, index=True)
    email: str = Field(unique=True, index=True, nullable=False)
    name: str = Field(nullable=False)
    # password_hash não é um campo Field pois será gerenciado pelo Supabase Auth,
    # ou se usarmos auth interno, seria um Field. Por enquanto,
    # vamos focar nos dados que armazenamos diretamente após a criação do usuário via Supabase Auth.
    # Se você for armazenar o hash no seu próprio DB, adicione:
    # password_hash: str = Field(nullable=False)
    role: str = Field(default="user", nullable=False)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)

    # Configuração para atualizar automaticamente 'updated_at' (pode ser feita via trigger no DB ou no serviço)
    # Para simplificar aqui, vamos deixá-lo com default_factory.
    # A atualização real em cada update será feita no serviço ou através de um trigger no DB.

    class Config:
        # Garante que os campos são populados mesmo se não fornecidos
        # (útil para campos com default_factory)
        populate_by_name = True