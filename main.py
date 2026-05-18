from fastapi import FastAPI
import requests
from sqlalchemy.orm import sessionmaker

from models import Linha
from database import db, Base

# Importa as rotas corretamente usando pseudónimos
from linhas_routes import router as linhas_router
from paradas_routes import router as paradas_router

app = FastAPI()

# Inclui as rotas na tua aplicação FastAPI
app.include_router(linhas_router)
app.include_router(paradas_router)

# Configuração da API Externa da SPTrans
token = "a8039497f56e36abb76cf6587c3458b11eb094481d2e41a7151270568e5128fe"
session_api = requests.Session()  # Corrigido: adicionados os parênteses ()

# Autenticação obrigatória na SPTrans
session_api.post(f"http://api.olhovivo.sptrans.com.br/v2.1/Login/Autenticar?token={token}")

# Configuração da Sessão do Banco de Dados (pronto para usar nas tuas rotas)
ConfigSessao = sessionmaker(bind=db)