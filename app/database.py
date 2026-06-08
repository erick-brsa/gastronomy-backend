import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Carga las variables desde el archivo .env al entorno de Python
load_dotenv()

# Obtiene la URL de la base de datos de manera segura
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("La variable de entorno DATABASE_URL no esta configurada.")

db_engine = create_async_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(
    bind=db_engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)

Base = declarative_base()

async def get_database_session():
    async with SessionLocal() as transaction_session:
        yield transaction_session