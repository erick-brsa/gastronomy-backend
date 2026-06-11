from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import db_engine, Base
from app.routers import health, recipe, auth

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title="Gastronomy API",
    description="API asincrona para la gestion y analisis inteligente de recetas de cocina",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(health.router)
app.include_router(recipe.router)
app.include_router(auth.router)