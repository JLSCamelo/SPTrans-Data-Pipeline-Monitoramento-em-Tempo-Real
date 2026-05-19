from database import db
from sqlalchemy.orm import sessionmaker
from models import Paradas
from fastapi import APIRouter, HTTPException
import requests
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/paradas", tags=["Paradas"])
token = os.getenv("SPTRANS_TOKEN")
ConfigSessao = sessionmaker(bind=db)

@router.post("/atualizar")
async def atualizar_paradas():
    """
    Rota que faz login na SPTrans, realiza uma varredura por tipos de logradouros
    para capturar o máximo de paradas da cidade sem duplicar, e atualiza o banco.db.
    """
    session_api = requests.Session()

    # 1. Autenticação obrigatória na API Olho Vivo
    try:
        auth_response = session_api.post(f"http://api.olhovivo.sptrans.com.br/v2.1/Login/Autenticar?token={token}")
        if auth_response.text.lower() != "true":
            raise HTTPException(status_code=401, detail="Falha na autenticação com a SPTrans. Verifique o token.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao conectar na SPTrans: {str(e)}")
    
    # 2. Varredura inteligente por tipos de vias para pegar a cidade toda
    paradas_unicas = {}  # Dicionário para remover duplicados usando o código da parada (cp)
    termos_busca = ["Av", "Rua", "Al", "Term"]

    try:
        for termo in termos_busca:
            resposta = session_api.get(f"http://api.olhovivo.sptrans.com.br/v2.1/Parada/Buscar?termosBusca={termo}")
            dados_busca = resposta.json()

            if dados_busca and isinstance(dados_busca, list):
                for item in dados_busca:
                    codigo_parada = item['cp']
                    # Só adiciona se o código da parada ainda não foi pego em outra busca
                    if codigo_parada not in paradas_unicas:
                        paradas_unicas[codigo_parada] = item
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Erro ao processar dados da API da SPTrans: {str(e)}")

    if not paradas_unicas:
        raise HTTPException(status_code=404, detail="Nenhuma parada encontrada na varredura da SPTrans.")

    # 3. Abre a conexão com o banco e faz a carga limpa (Overwrite)
    banco = ConfigSessao()
    paradas_salvas = 0

    try:
        # Limpa as paradas antigas para evitar chaves duplicadas ou banco inflado
        banco.query(Paradas).delete()

        for item in paradas_unicas.values():
            nova_parada = Paradas(
                id=item['cp'],
                nome_parada=item['np'],
                endereco=item.get('ed', 'Endereço não informado'),
                latitude=float(item['py']), # Agora vai funcionar!
                longitude=float(item['px'])
            )
            banco.add(nova_parada)
            paradas_salvas += 1

        banco.commit()
        return {"status": "sucesso", "mensagem": f"Varredura de paradas concluída! {paradas_salvas} paradas únicas importadas."}
    except Exception as e:
        banco.rollback()
        print("\n" + "="*50)
        print(f"ERRO: DO BANCO (PARADAS): {e}")
        # ISSO AQUI VAI MOSTRAR OS NOMES DAS SUAS COLUNAS:
        try:
            colunas = [c.name for c in Paradas.__table__.columns]
            print(f"As colunas que existem no seu Model são: {colunas}")
        except:
            pass
        print("="*50 + "\n")
        raise HTTPException(status_code=500, detail=f"Erro ao salvar no banco de dados: {str(e)}")
    finally:
        banco.close()

@router.get("/")
async def buscar_paradas():
    banco = ConfigSessao()
    try:
        paradas = banco.query(Paradas).all()
        return paradas
    finally:
        #fechar conexão com o banco
        banco.close()


@router.get("/buscar/{nome}")
async def buscar_parada_nome(nome: str):
    #abre sessão com o banco
    banco=ConfigSessao()
    try:
        paradas = banco.query(Paradas).filter(Paradas.nome_parada.contains(nome)).all()
        if not paradas:
            raise HTTPException(status_code=404, detail="Nenhuma parada encontrada.")
        return paradas
    finally:
        #fechya conexão com banco
        banco.close()


@router.get("/{parada_id}")
async def buscar_parada_id(parada_id: int):#Cria função para buscar, e após coloca o int como o valor do id
    #Abre sessão no banco
    banco=ConfigSessao()
    try: 
        parada = banco.query(Paradas).filter(Paradas.id == parada_id).first()
        if not parada: # Se não encontrar a parada ou estuver vazio, retorna erro 404
            raise HTTPException(status_code=404, detail="Parada não encontrada")
        return parada
    finally:
        #fecha conexão com o banco
        banco.close()


    
