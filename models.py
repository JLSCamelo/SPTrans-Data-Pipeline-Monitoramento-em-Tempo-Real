from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey#Permissao de conectar uma tabela em outra tabela
from sqlalchemy.orm import declarative_base, sessionmaker
from database import Base


#cria a conexão com o banco
db = create_engine("sqlite:///banco.db")
#cria a base do mando de dados
Base = declarative_base()
#cria as classes/tabelas do banco

#criação de classes e tabelas
class Linha(Base):
    __tablename__="linhas"#definindo nome

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    # primary_key=True: Define o "CPF" do registro (identificador único obrigatório).
    # autoincrement=True: Faz o MySQL gerar o próximo número (1, 2, 3...) sozinho.
    numero = Column("numero", String)
    empresa = Column("empresa", String)
    area = Column("area", String)
    terminal_inicial = Column("terminal_inicial", String)
    terminal_final = Column("terminal_final", String)

    def __init__(self, numero, empresa, area, terminal_inicial, terminal_final):
        self.numero = numero
        self.empresa = empresa
        self.area = area
        self.terminal_inicial = terminal_inicial
        self.terminal_final = terminal_final
    

class Paradas(Base):
    __tablename__="paradas"
    id = Column("id", Integer, primary_key=True, autoincrement=True)

    nome_parada = Column("nome_parada", String)
    endereco = Column("endereco", String)
    latitude = Column("latitude", Float)
    longitude = Column("longitude", Float)

class veiculos(Base):
    __tablename__="veiculos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    prefixo=Column("prefixo", Integer)
    latitude=Column("latitude", Float)
    longitude = Column("longitude", Float)

class previsoes(Base):
    __tablename__="previsoes"
    id = Column(Integer, primary_key=True, autoincrement=True)

    veiculo_id = Column(Integer, ForeignKey("veiculos.id"))
    parada_id = Column(Integer, ForeignKey("paradas.id"))
    tempo_chegada = Column(String)

