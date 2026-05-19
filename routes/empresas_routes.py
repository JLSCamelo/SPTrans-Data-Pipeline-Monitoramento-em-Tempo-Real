from fastapi import APIRouter, HTTPException
import requests
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/empresas", tags=["Empresas"])
token = os.getenv("SPTRANS_TOKEN")

def autenticar_sptrans():
    session_api = requests.Session()
    
    resposta = session_api.post(
        f"https://api.olhovivo.sptrans.com.br/v2.1/Login/Autenticar?token={token}"
    )

    if resposta.text.lower() != "true":
        raise HTTPException(status_code=401, detail="Falha na autenticação.")
    return session_api

@router.get("/")
async def buscar_empresas():
    #iniciar sessão
    session_api = autenticar_sptrans()

    resposta = session_api.get(
        f"http://api.olhovivo.sptrans.com.br/v2.1/Empresa"
    )
    return resposta.json()



    