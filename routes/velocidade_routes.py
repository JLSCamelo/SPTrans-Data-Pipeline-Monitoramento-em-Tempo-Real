from fastapi import APIRouter, HTTPException, Response
import requests
import os
from dotenv import load_dotenv

router = APIRouter(prefix="/velocidade", tags=["Velocidade nas vias"])

token = os.getenv("SPTRANS_TOKEN")


def autenticar_sptrans():
    session_api = requests.Session()

    resposta = session_api.post(
        f"https://api.olhovivo.sptrans.com.br/v2.1/Login/Autenticar?token={token}"
    )

    if resposta.text.lower() != "true":
        raise HTTPException(status_code=401, detail="Falha na autenticação com a SPTrans")

    return session_api


@router.get("/")
async def velocidade_geral():
    session_api = autenticar_sptrans()

    resposta = session_api.get(
        "https://api.olhovivo.sptrans.com.br/v2.1/KMZ"
    )

    return Response(
        content=resposta.content,
        media_type="application/vnd.google-earth.kmz"
    )


@router.get("/sentido/{sentido}")
async def velocidade_por_sentido(sentido: str):
    session_api = autenticar_sptrans()

    sentido = sentido.upper()

    if sentido not in ["BC", "CB"]:
        raise HTTPException(
            status_code=400,
            detail="Sentido inválido. Use BC ou CB."
        )

    resposta = session_api.get(
        f"https://api.olhovivo.sptrans.com.br/v2.1/KMZ/{sentido}"
    )

    return Response(
        content=resposta.content,
        media_type="application/vnd.google-earth.kmz"
    )


@router.get("/corredor")
async def velocidade_corredores():
    session_api = autenticar_sptrans()

    resposta = session_api.get(
        "https://api.olhovivo.sptrans.com.br/v2.1/KMZ/Corredor"
    )

    return Response(
        content=resposta.content,
        media_type="application/vnd.google-earth.kmz"
    )


@router.get("/corredor/{sentido}")
async def velocidade_corredor_por_sentido(sentido: str):
    session_api = autenticar_sptrans()

    sentido = sentido.upper()

    if sentido not in ["BC", "CB"]:
        raise HTTPException(
            status_code=400,
            detail="Sentido inválido. Use BC ou CB."
        )

    resposta = session_api.get(
        f"https://api.olhovivo.sptrans.com.br/v2.1/KMZ/Corredor/{sentido}"
    )

    return Response(
        content=resposta.content,
        media_type="application/vnd.google-earth.kmz"
    )


@router.get("/outras-vias")
async def velocidade_outras_vias():
    session_api = autenticar_sptrans()

    resposta = session_api.get(
        "https://api.olhovivo.sptrans.com.br/v2.1/KMZ/OutrasVias"
    )

    return Response(
        content=resposta.content,
        media_type="application/vnd.google-earth.kmz"
    )


@router.get("/outras-vias/{sentido}")
async def velocidade_outras_vias_por_sentido(sentido: str):
    session_api = autenticar_sptrans()

    sentido = sentido.upper()

    if sentido not in ["BC", "CB"]:
        raise HTTPException(
            status_code=400,
            detail="Sentido inválido. Use BC ou CB."
        )

    resposta = session_api.get(
        f"https://api.olhovivo.sptrans.com.br/v2.1/KMZ/OutrasVias/{sentido}"
    )

    return Response(
        content=resposta.content,
        media_type="application/vnd.google-earth.kmz"
    )