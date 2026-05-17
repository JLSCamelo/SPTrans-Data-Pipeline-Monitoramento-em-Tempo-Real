from fastapi import APIRouter

linhas_routes = APIRouter(prefix="/linhas", tags=["Linhas"])

@linhas_routes.get("/buscar")
async def linhas():
    return {"Mensagem": "você acessou a rota de linhas", "autenticado": False}
