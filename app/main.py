from fastapi import FastAPI

app = FastAPI(
    title="Gastronomy API",
    description="API asincrona para la gestion y analisis inteligente de recetas de cocina",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"status": "healthy", "message": "Servidor de recetas activo"}