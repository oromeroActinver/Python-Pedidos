from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from database import get_db
from models import Pedido
from schemas import PedidoCreate, PedidoOut, PedidoUpdate

router = APIRouter(
    prefix="/pedidos",
    tags=["pedidos"],
    redirect_slashes=False
)

# Endpoint único para listar pedidos (sin duplicados)
@router.get(
    "",
    response_model=List[PedidoOut],
    summary="Listar pedidos",
    description="Obtiene lista paginada de pedidos"
)
async def listar_pedidos(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    try:
        pedidos = db.query(Pedido).offset(skip).limit(limit).all()
        return [
            {
                "id": p.id,
                "pedido": p.pedido,
                "cliente": p.cliente,
                "tienda": p.tienda,
                "descripcion": p.descripcion,
                "estado": p.estado,
                "costo": p.costo,
                "created_at": p.created_at if hasattr(p, 'created_at') else None,
                "updated_at": p.updated_at if hasattr(p, 'updated_at') else None
            }
            for p in pedidos
        ]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener pedidos: {str(e)}"
        )

# 🔥 NUEVO: Endpoint para crear pedidos (POST)
@router.post(
    "",
    response_model=PedidoOut,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nuevo pedido"
)
async def crear_pedido(
    pedido: PedidoCreate,
    db: Session = Depends(get_db)
):
    try:
        # Convertir el modelo Pydantic a diccionario
        pedido_data = pedido.dict()
        
        # Crear instancia del modelo SQLAlchemy
        nuevo_pedido = Pedido(**pedido_data)
        
        db.add(nuevo_pedido)
        db.commit()
        db.refresh(nuevo_pedido)
        
        return nuevo_pedido
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear pedido: {str(e)}"
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