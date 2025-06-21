from sqlmodel import create_engine, Session
from app.core.config import get_settings

# Carregar configurações
settings = get_settings()

# Criar o motor do banco de dados
# echo=True é útil para depuração, pois mostra as queries SQL geradas
engine = create_engine(settings.DATABASE_URL, echo=True)

def create_db_and_tables():
    # Importe todos os modelos SQLModel aqui para que o metadata seja preenchido
    # antes de chamar create_all()
    # Isso será feito nos próximos passos quando você criar os modelos.
    # Ex: from app.models.user import User
    # from app.models.post import Post
    # from app.models.media import Media

    # SQLModel.metadata.create_all(engine) # descomente quando tiver seus modelos definidos

    # Por enquanto, apenas para garantir que o engine está funcionando
    # Em produção, o Supabase já terá as tabelas criadas.
    pass 

def get_session():
    with Session(engine) as session:
        yield session