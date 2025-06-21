from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router

settings = get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Configuração do CORS Middleware
# Permite requisições de qualquer origem, para facilitar o desenvolvimento frontend
# Em produção, você deve restringir 'origins' apenas aos domínios do seu frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permite todos os headers
)

@app.get("/")
def read_root():
    return {"message": "Bem-vindo ao Social Media Content Manager API!"}

# Incluir o router de autenticação
app.include_router(auth_router, prefix=settings.API_V1_STR) 
app.include_router(users_router, prefix=settings.API_V1_STR)

# Você adicionará os routers de API aqui posteriormente:
# from app.api.v1.auth import router as auth_router
# app.include_router(auth_router, prefix=settings.API_V1_STR)

# from app.api.v1.posts import router as posts_router
# app.include_router(posts_router, prefix=settings.API_V1_STR)

# ... e assim por diante para outros routers