from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str


# Esquemas para productos
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductOut(ProductBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

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
    model_config = ConfigDict(from_attributes=True)

# Esquema para respuesta de lista de pedidos
class PedidoList(BaseModel):
    pedidos: List[PedidoOut]
