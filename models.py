from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
from datetime import datetime

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

class Pedido(Base):
    __tablename__ = "pedidos"
    id = Column(Integer, primary_key=True, index=True)
    pedido = Column(String(50), unique=True, nullable=False)
    cliente = Column(String(100), nullable=False)
    tienda = Column(String(50), nullable=False)
    descripcion = Column(String(500))
    estado = Column(String(20), default="pendiente", nullable=False)
    costo = Column(Float, nullable=False)
    envio = Column(Float, default=0.0, server_default="0.0", nullable=False)
    costo_compra = Column(Float, default=0.0, server_default="0.0", nullable=False)

class Resumen(Base):
    __tablename__ = "resumenes"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime, default=datetime.utcnow)
    totalVentas = Column(Float, default=0.0)
    totalCostos = Column(Float, default=0.0)
    ganancia = Column(Float, default=0.0)
    comision = Column(Float, default=0.0)
    impuestosCliente = Column(Float, default=0.0)
    impuestosProveedor = Column(Float, default=0.0)
    abono = Column(Float, default=0.0)
    descuentos = Column(Float, default=0.0)
    detalles = relationship("DetalleResumen", back_populates="resumen")



class DetalleResumen(Base):
    __tablename__ = "detalle_resumenes"
    id = Column(Integer, primary_key=True, index=True)
    resumen_id = Column(Integer, ForeignKey("resumenes.id"))
    pedido = Column(String)
    cliente = Column(String)
    venta = Column(Float)
    costo = Column(Float)
    envio = Column(Float)
    resumen = relationship("Resumen", back_populates="detalles")

