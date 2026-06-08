# Gastronomy API

API asincrona de alto rendimiento desarrollada en Python con FastAPI para la gestion estructurada, escalado y busqueda inteligente de recetas de cocina.

## Arquitectura del Proyecto

El proyecto sigue una estructura limpia y modular estructurada por capas para separar responsabilidades de forma estricta:

- **app/models/**: Definicion de las tablas de la base de datos utilizando el ORM SQLAlchemy.
- **app/schemas/**: Modelos de validacion y serializacion de datos de entrada y salida mediante Pydantic.
- **app/routers/**: Endpoints de la API divididos por modulos utilizando APIRouter de FastAPI.
- **app/crud/**: Logica de persistencia y consultas optimizadas a la base de datos relacional.
- **app/main.py**: Punto de entrada de la aplicacion y configuracion del servidor.

## Requisitos Previos

Asegurate de tener instalado Python 3.10 o superior y PostgreSQL.

## Instalacion y Clonado Local

### 1. Crear y activar el entorno virtual de Python:
```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 2. Instalar las dependencias requeridas:
```bash
pip install -r requirements.txt
```


### 3. Levantar el servidor de desarrollo local con recarga automatica:
```bash
uvicorn app.main:app --reload
```



El servidor estara disponible en http://127.0.0.1:8000 y podras acceder a la documentacion interactiva autogenerada en http://127.0.0.1:8000/docs.
