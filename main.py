from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth import router as auth_router
from pedidos import router as pedidos_router
from database import Base, engine
from models import User, Product, Pedido

Base.metadata.create_all(bind=engine)


Base.metadata.create_all(bind=engine)


app = FastAPI()
origins = os.getenv("ALLOWED_ORIGINS", "").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

# Incluimos el router con prefijo /auth
app.include_router(auth_router, prefix="/auth")
app.include_router(pedidos_router)

@app.get("/")
def read_root():
    return {"mensaje": "¡FastAPI funcionando correctamente!"}


   
