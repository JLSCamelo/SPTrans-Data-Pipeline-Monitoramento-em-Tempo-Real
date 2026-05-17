from fastapi import APIRouter

paradas_routes = APIRouter(prefix="/paradas", tags=["Paradas"]) #criar um prefixo padrao para todas as rotas

@paradas_routes.get("/buscar")
async def paradas():
    return{"Mensagem": "Você acessou a buscar de paradas"}