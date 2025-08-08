from sqlalchemy import Column, Integer, String, Float, DateTime  # Añade DateTime aquí
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    price = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relación opcional con pedidos (si los pedidos incluyen productos)
    # pedidos = relationship("Pedido", secondary="pedido_productos", back_populates="products")

class Pedido(Base):
    __tablename__ = "pedidos"
    
    id = Column(Integer, primary_key=True, index=True)
    pedido = Column(String(50), unique=True, nullable=False)
    cliente = Column(String(100), nullable=False)
    tienda = Column(String(50), nullable=False)
    descripcion = Column(String(500))
    estado = Column(String(20), default="pendiente", nullable=False)
    costo = Column(Float, nullable=False)
