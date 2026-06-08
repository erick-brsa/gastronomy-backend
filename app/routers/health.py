# app/routers/health.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.database import get_database_session

# APIRouter nos permite crear mini-aplicaciones modulares
router = APIRouter(tags=["System Health"])

@router.get("/health", summary="Verificar estado del sistema")
async def check_health(db_session: AsyncSession = Depends(get_database_session)):
    try:
        await db_session.execute(text("SELECT 1"))
        return {
            "status": "operativo",
            "database_connection": "exitosa",
            "message": "La API y PostgreSQL estan comunicandose correctamente."
        }
    except Exception as error_details:
        return {
            "status": "falla",
            "database_connection": "caida",
            "error": str(error_details)
        }