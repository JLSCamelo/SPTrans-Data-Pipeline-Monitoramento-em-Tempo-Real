import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

engine_url = os.getenv("DATABASE_URL", "sqlite:///banco.db")

db = create_engine(engine_url, connect_args={"check_same_thread": False})

Base = declarative_base()