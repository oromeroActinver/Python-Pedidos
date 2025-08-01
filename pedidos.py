from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from database import get_db  # función para obtener sesión DB
from models import Pedido    # modelo ORM
from schemas import PedidoIn, PedidoOut  # esquemas Pydantic

router = APIRouter()

@router.post("/pedidos", response_model=PedidoOut)
def crear_pedido(pedido: PedidoIn, db: Session = Depends(get_db)):
    nuevo_pedido = Pedido(**pedido.dict())
    db.add(nuevo_pedido)
    db.commit()
    db.refresh(nuevo_pedido)  # para obtener el id autogenerado
    return nuevo_pedido

@router.get("/pedidos", response_model=List[PedidoOut])
def listar_pedidos(db: Session = Depends(get_db)):
    pedidos = db.query(Pedido).all()
    return pedidos

@router.put("/pedidos/{pedido_id}", response_model=PedidoOut)
def actualizar_pedido(pedido_id: int, pedido: PedidoIn, db: Session = Depends(get_db)):
    pedido_db = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido_db:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    for key, value in pedido.dict().items():
        setattr(pedido_db, key, value)
    db.commit()
    db.refresh(pedido_db)
    return pedido_db

@router.delete("/pedidos/{pedido_id}")
def eliminar_pedido(pedido_id: int, db: Session = Depends(get_db)):
    pedido_db = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido_db:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    db.delete(pedido_db)
    db.commit()
    return {"mensaje": "Pedido eliminado correctamente"}
