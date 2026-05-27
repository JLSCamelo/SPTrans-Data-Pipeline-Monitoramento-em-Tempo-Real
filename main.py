from fastapi import FastAPI
import requests
from sqlalchemy.orm import sessionmaker
from fastapi.middleware.cors import CORSMiddleware
from models import Linha
from database import db, Base

# Importa as rotas corretamente usando pseudónimos
from routes.linhas_routes import router as linhas_router
from routes.paradas_routes import router as paradas_router
from routes.previsao_routes import router as previsao_router
from routes.empresas_routes import router as empresas_router
from routes.velocidade_routes import router as velocidade_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui as rotas na tua aplicação FastAPI
app.include_router(linhas_router)
app.include_router(paradas_router)
app.include_router(previsao_router, prefix="/previsoes")
app.include_router(empresas_router)
app.include_router(velocidade_router)

# Configuração da API Externa da SPTrans
token = "a8039497f56e36abb76cf6587c3458b11eb094481d2e41a7151270568e5128fe"
session_api = requests.Session()  # Corrigido: adicionados os parênteses ()

# Autenticação obrigatória na SPTrans
session_api.post(f"http://api.olhovivo.sptrans.com.br/v2.1/Login/Autenticar?token={token}")

# Configuração da Sessão do Banco de Dados (pronto para usar nas tuas rotas)
ConfigSessao = sessionmaker(bind=db)