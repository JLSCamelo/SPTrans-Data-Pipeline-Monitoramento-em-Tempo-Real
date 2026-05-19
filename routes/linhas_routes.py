from database import db
from sqlalchemy.orm import sessionmaker
from models import Linha
from fastapi import APIRouter, HTTPException
import requests
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("SPTRANS_TOKEN")
router = APIRouter(prefix="/linhas", tags=["Linhas"])

ConfigSessao = sessionmaker(bind=db)

@router.post("/atualizar")
async def atualizar_linhas():
    """
    Rota que faz login na SPTrans, varre os dígitos de 0 a 9 para capturar
    todas as linhas do sistema sem duplicar, e atualiza o banco.db.
    """
    session_api = requests.Session()
    
    # 1. Autenticação obrigatória na API Olho Vivo
    try:
        auth_response = session_api.post(f"http://api.olhovivo.sptrans.com.br/v2.1/Login/Autenticar?token={token}")
        if auth_response.text.lower() != "true":
            raise HTTPException(status_code=401, detail="Falha na autenticação com a SPTrans. Verifique o Token.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao conectar na SPTrans: {str(e)}")

    # 2. Varredura inteligente para pegar todas as linhas de 0 a 9
    linhas_unicas = {} # Dicionário temporário para remover duplicados usando o código da linha (cl) como chave
    
    try:
        # Varre os dígitos de 0 a 9 para cobrir todas as combinações de linhas
        for digito in range(10):
            resposta = session_api.get(f"http://api.olhovivo.sptrans.com.br/v2.1/Linha/Buscar?termosBusca={digito}")
            dados_busca = resposta.json()
            
            if dados_busca and isinstance(dados_busca, list):
                for item in dados_busca:
                    # Se a linha ainda não foi capturada nesta rodada, adiciona ao dicionário
                    codigo_linha = item['cl']
                    if codigo_linha not in linhas_unicas:
                        linhas_unicas[codigo_linha] = item
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Erro ao processar dados da API da SPTrans: {str(e)}")
    
    if not linhas_unicas:
        raise HTTPException(status_code=404, detail="Nenhuma linha encontrada na varredura da SPTrans.")
        
    # 3. Abre a conexão com o banco e faz a carga limpa (Overwrite)
    banco = ConfigSessao()
    linhas_salvas = 0
    
    try:
        # Limpa os dados antigos antes de carregar a malha inteira
        banco.query(Linha).delete()

        for item in linhas_unicas.values():
            nova_linha = Linha(
                numero=f"{item['lt']}-{item['sl']}", # lt (Letreiro) e sl (Sentido)
                empresa="SPTrans",
                area=str(item['cl']),                # cl (Código identificador da linha)
                terminal_inicial=item['tp'],         # tp (Letreiro Terminal Principal)
                terminal_final=item['ts']            # ts (Letreiro Terminal Secundário)
            )
            banco.add(nova_linha)
            linhas_salvas += 1
            
        banco.commit()
        return {"status": "sucesso", "mensagem": f"Varredura concluída! {linhas_salvas} linhas únicas importadas para o banco."}
        
    except Exception as e:
        banco.rollback()
        print("\n" + "="*50)
        print(f"ERRO REAL DO BANCO: {e}")
        print("="*50 + "\n")
        raise HTTPException(status_code=500, detail=f"Erro ao salvar no banco de dados: {str(e)}")
    finally:
        banco.close()


@router.get("/")
async def listar_linhas():
    #Abre uma sessão com o banco
    banco=ConfigSessao()

    try:
        #busca todas as linhas na tabela linha
        linhas = banco.query(Linha).all()
        return linhas
    finally:
        #fecha a conexão com o banco
        banco.close


@router.get("/buscar/{numero}")
async def buscar_linha_numero(numero: str):
    #Abre uma sessão com o banco
    banco = ConfigSessao()

    try:
        #busca lingas cujo campo numero contenha o texto informado
        linhas = banco.query(Linha).filter(Linha.numero.contains(numero)).all()

        #se a lista estiver vazia retorna erro
        if not linhas:
            raise HTTPException(status_code=404, detail="Nenhuma linha encontrada")
        #retorna todas as linhas encontradas
        return linhas
    finally:
        #fecha conexão com o banco
        banco.close()



router.get("/{linha_id}")
async def buscar_linha_id(linha_id: int):
    #abre uma sessão com o banco
    banco = ConfigSessao()

    try:
        #Busca a Linha cujo seja igual ao Linha_id recebido na url
        linha = banco.query(Linha).filter(Linha.id == linha_id).first()

        #se não encontrar, retorna erro 404
        if not linha:
            raise HTTPException(status_code=404, detail="Linha não encontrada")
        #se encontrar, retorna a linha
        return linha
    
    finally:
        #fecha a conexão com o banco
        banco.close()

