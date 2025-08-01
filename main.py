from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth import router as auth_router
from pedidos import router as pedidos_router
from database import Base, engine
from models import User, Product, Pedido

Base.metadata.create_all(bind=engine)


Base.metadata.create_all(bind=engine)


app = FastAPI()

# Orígenes permitidos (URL de tu frontend)
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",  # o la URL donde tengas tu frontend
    "http://tu-dominio.com"
]

# Agregamos el middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       #origins,      # o ["*"] para desarrollo sin restricciones
    allow_credentials=True,
    allow_methods=["*"],        # permite GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],        # permite cualquier encabezado
)

# Incluimos el router con prefijo /auth
app.include_router(auth_router, prefix="/auth")
app.include_router(pedidos_router)

@app.get("/")
def read_root():
    return {"mensaje": "¡FastAPI funcionando correctamente!"}


   
