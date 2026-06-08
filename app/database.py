import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Carga las variables desde el archivo .env al entorno de Python
load_dotenv()

# Obtiene la URL de la base de datos de manera segura
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("La variable de entorno DATABASE_URL no esta configurada.")

db_engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)

Base = declarative_base()

def get_database_session():
    transaction_session = SessionLocal()
    try:
        yield transaction_session
    finally:
        transaction_session.close()