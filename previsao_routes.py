from fastapi import APIRouter, HTTPException
import requests


router=APIRouter(prefix="/previsoes", tags="Previsões")
token="a8039497f56e36abb76cf6587c3458b11eb094481d2e41a7151270568e5128fe" \

def autenticar_sptrans():
    session_api = requests.Session()

    resposta = session_api.post(
        f"http://api.olhovivo.sptrans.com.br/v2.1/Login/Autenticar?token={token}"
    )

    if resposta.text.lower() != "true":
        raise HTTPException(status_code=401, detail="Falha na autenticação.")
    return session_api

@router.get("/")
async def listar_previsoes():
    #iniciar sessão
    session_api = autenticar_sptrans()

    resposta = session_api.get(
        f"http://api.olhovivo.sptrans.com.br/v2.1/Previsao"
    )
    return resposta.json()

@router.get("linha/{codigo_linha}")
async def previsao_linha(codigo_linha: int):
    session_api = autenticar_sptrans()

    resposta = session_api(
        f"http://api.olhovivo.sptrans.com.br/v2.1/Previsao/Linha?codigoLinha={codigo_linha}"
    )
    return resposta.json()

@router.get("parada/{codigo_parada}")
async def previsao_parada(codigo_parada: int):
    session_api = autenticar_sptrans()

    resposta = session_api(
        f"http://api.olhovivo.sptrans.com.br/v2.1/Previsao/Parada?codigoParada={codigo_parada}"
    )
    return resposta.json()


