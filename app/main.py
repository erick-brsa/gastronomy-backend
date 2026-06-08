from fastapi import FastAPI
from app.database import db_engine, Base
from app.routers import health

# TODO: Eliminar cuando se implemente Alembic para migraciones
Base.metadata.create_all(bind=db_engine)

app = FastAPI(
    title="Gastronomy API",
    description="API asincrona para la gestion y analisis inteligente de recetas de cocina",
    version="1.0.0"
)

# Conectamos el enrutador modular a la aplicacion principal
app.include_router(health.router)