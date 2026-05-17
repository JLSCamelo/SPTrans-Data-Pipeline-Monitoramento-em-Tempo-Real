from fastapi import FastAPI

app=FastAPI()
#uvicorn main:app --reload
from linhas_routes import linhas_routes
from paradas_routes import paradas_routes

app.include_router(linhas_routes)
app.include_router(paradas_routes)

 