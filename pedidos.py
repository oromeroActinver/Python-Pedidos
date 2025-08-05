from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from database import get_db
from models import Pedido
from schemas import PedidoCreate, PedidoOut, PedidoUpdate

router = APIRouter(prefix="/pedidos", tags=["pedidos"])

@router.get("/", response_model=List[PedidoOut])
async def listar_pedidos(db: Session = Depends(get_db)):
    try:
        pedidos = db.query(Pedido).all()
        
        # Asegurar compatibilidad con campos opcionales
        result = []
        for p in pedidos:
            pedido_data = {
                "id": p.id,
                "pedido": p.pedido,
                "cliente": p.cliente,
                "tienda": p.tienda,
                "descripcion": p.descripcion,
                "estado": p.estado,
                "costo": p.costo
            }
            # Agregar campos opcionales solo si existen
            if hasattr(p, 'created_at'):
                pedido_data['created_at'] = p.created_at
            if hasattr(p, 'updated_at'):
                pedido_data['updated_at'] = p.updated_at
            
            result.append(pedido_data)
        
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener pedidos: {str(e)}"
        )

@router.get(
    "/",
    response_model=List[PedidoOut],
    summary="Listar todos los pedidos"
)
async def listar_pedidos(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    Obtiene una lista de todos los pedidos registrados.
    """
    try:
        pedidos = db.query(Pedido).offset(skip).limit(limit).all()
        return pedidos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener pedidos: {str(e)}"
        )

@router.get(
    "/{pedido_id}",
    response_model=PedidoOut,
    summary="Obtener un pedido específico"
)
async def obtener_pedido(
    pedido_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtiene los detalles de un pedido específico por su ID.
    """
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pedido con ID {pedido_id} no encontrado"
        )
    return pedido

@router.put(
    "/{pedido_id}",
    response_model=PedidoOut,
    summary="Actualizar un pedido completo"
)
async def actualizar_pedido(
    pedido_id: int,
    pedido: PedidoCreate,
    db: Session = Depends(get_db)
):
    """
    Actualiza todos los campos de un pedido existente.
    """
    try:
        pedido_db = db.query(Pedido).filter(Pedido.id == pedido_id).first()
        if not pedido_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pedido no encontrado"
            )
        
        # Usamos .dict() para Pydantic v1
        update_data = pedido.dict()
        for key, value in update_data.items():
            setattr(pedido_db, key, value)
        
        db.commit()
        db.refresh(pedido_db)
        return pedido_db
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar pedido: {str(e)}"
        )

@router.delete(
    "/{pedido_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un pedido"
)
async def eliminar_pedido(
    pedido_id: int,
    db: Session = Depends(get_db)
):
    """
    Elimina un pedido existente del sistema.
    """
    try:
        pedido_db = db.query(Pedido).filter(Pedido.id == pedido_id).first()
        if not pedido_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pedido no encontrado"
            )
        
        db.delete(pedido_db)
        db.commit()
        return None
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar pedido: {str(e)}"
        )