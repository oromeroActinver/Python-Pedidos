from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

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

from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class PedidoBase(BaseModel):
    pedido: str
    cliente: str
    tienda: str
    descripcion: str
    estado: str
    costo: float
    envio: float = 0.0  # No Optional
    costo_compra: float = 0.0  # No Optional

class PedidoCreate(PedidoBase):
    pass

class PedidoUpdate(BaseModel):
    pedido: Optional[str] = None
    cliente: Optional[str] = None
    tienda: Optional[str] = None
    descripcion: Optional[str] = None
    estado: Optional[str] = None
    costo: Optional[float] = None
    envio: Optional[float] = None
    costo_compra: Optional[float] = None

class PedidoOut(PedidoBase):
    id: int
    created_at: Optional[datetime] = None  # Campo opcional
    updated_at: Optional[datetime] = None  # Campo opcional
    
    class Config:
        orm_mode = True
        # Para Pydantic v2 usa:
        # from pydantic import ConfigDict
        # model_config = ConfigDict(from_attributes=True)

class PedidoList(BaseModel):
    pedidos: List[PedidoOut]