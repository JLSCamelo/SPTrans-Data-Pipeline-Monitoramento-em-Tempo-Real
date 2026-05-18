from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

# Cria a conexão com o arquivo banco.db
engine_url = "sqlite:///banco.db"
db = create_engine(engine_url, connect_args={"check_same_thread": False})

# O Base é o molde que o SQLAlchemy usa para criar as tabelas
Base = declarative_base()