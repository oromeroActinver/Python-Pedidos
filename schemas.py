from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str


class PedidoIn(BaseModel):
    pedido: str
    cliente: str
    tienda: str
    descripcion: str
    estado: str
    costo: float

class PedidoOut(PedidoIn):
    id: int

    class Config:
        from_attributes = True  # Para Pydantic v2, antes era orm_mode = True
