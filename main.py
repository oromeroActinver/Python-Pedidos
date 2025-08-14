import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine

# Importa routers DESPUÉS de crear la base de datos
from auth import router as auth_router
from pedidos import router as pedidos_router

# Solución para errores de importación circular
def create_tables():
    Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configura CORS de forma segura
origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "https://python-pedidos.onrender.com",
    "https://react-compras.onrender.com"
] + os.getenv("ALLOWED_ORIGINS", "").split(",")

# Configuración CORS más estricta
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción especifica tus dominios
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["Content-Length"],
    max_age=600
)

# Crea tablas antes de los routers
create_tables()

# Registra routers
app.include_router(auth_router, prefix="/auth")
app.include_router(pedidos_router)

@app.get("/")
def read_root():
    return {"mensaje": "¡API funcionando!"}