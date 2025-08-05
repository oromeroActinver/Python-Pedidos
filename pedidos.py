from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List, Annotated
from datetime import datetime

from database import get_db
from models import Pedido
from schemas import PedidoCreate, PedidoOut, PedidoUpdate

router = APIRouter(prefix="/pedidos", tags=["pedidos"])

@router.post(
    "/",
    response_model=PedidoOut,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo pedido"
)
async def crear_pedido(
    pedido: PedidoCreate,
    db: Session = Depends(get_db)
):
    """
    Crea un nuevo pedido en el sistema.
    
    - **pedido**: Número/identificador del pedido
    - **cliente**: Nombre del cliente
    - **tienda**: Tienda/origen del pedido
    - **descripcion**: Detalles del pedido
    - **estado**: Estado actual (pendiente, completado, etc)
    - **costo**: Monto total del pedido
    """
    try:
        nuevo_pedido = Pedido(**pedido.model_dump())
        db.add(nuevo_pedido)
        db.commit()
        db.refresh(nuevo_pedido)
        return nuevo_pedido
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el pedido: {str(e)}"
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
    
    Parámetros opcionales:
    - **skip**: Número de registros a saltar (paginación)
    - **limit**: Límite de registros a devolver
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
        
        for key, value in pedido.model_dump().items():
            setattr(pedido_db, key, value)
        
        pedido_db.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(pedido_db)
        return pedido_db
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar pedido: {str(e)}"
        )

@router.patch(
    "/{pedido_id}",
    response_model=PedidoOut,
    summary="Actualizar parcialmente un pedido"
)
async def actualizar_parcial_pedido(
    pedido_id: int,
    pedido: PedidoUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualiza campos específicos de un pedido existente.
    """
    try:
        pedido_db = db.query(Pedido).filter(Pedido.id == pedido_id).first()
        if not pedido_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pedido no encontrado"
            )
        
        update_data = pedido.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(pedido_db, key, value)
        
        pedido_db.updated_at = datetime.utcnow()
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