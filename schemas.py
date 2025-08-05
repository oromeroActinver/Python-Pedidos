from pydantic import BaseModel
from typing import Optional, List

# Esquemas para usuarios
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserLogin(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    
    class Config:
        orm_mode = True  # Configuración para Pydantic v1

# Esquemas para productos
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductOut(ProductBase):
    id: int
    
    class Config:
        orm_mode = True

# Esquemas para pedidos
class PedidoBase(BaseModel):
    pedido: str
    cliente: str
    tienda: str
    descripcion: str
    estado: str
    costo: float

class PedidoCreate(PedidoBase):
    pass

class PedidoUpdate(BaseModel):
    pedido: Optional[str] = None
    cliente: Optional[str] = None
    tienda: Optional[str] = None
    descripcion: Optional[str] = None
    estado: Optional[str] = None
    costo: Optional[float] = None

class PedidoOut(PedidoBase):
    id: int
    
    class Config:
        orm_mode = True

# Esquema para respuesta de lista de pedidos
class PedidoList(BaseModel):
    pedidos: List[PedidoOut]