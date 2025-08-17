# resumenes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models import Resumen, DetalleResumen
from schemas import ResumenSchema
from database import get_db

router = APIRouter()  # <- IMPORTANTE: usar router, no app

@router.get("/resumenes", response_model=List[ResumenSchema])
def obtener_resumenes(db: Session = Depends(get_db)):
    res = db.query(Resumen).all()
    return res

@router.get("/resumenes/{resumen_id}", response_model=ResumenSchema)
def obtener_resumen(resumen_id: int, db: Session = Depends(get_db)):
    res = db.query(Resumen).filter(Resumen.id == resumen_id).first()
    if not res:
        raise HTTPException(status_code=404, detail="Resumen no encontrado")
    return res

@router.post("/resumenes")
def crear_resumen(resumen: ResumenSchema, db: Session = Depends(get_db)):
    res_db = Resumen(
    fecha=resumen.fecha,
    totalVentas=resumen.totalVentas,
    totalCostos=resumen.totalCostos,
    ganancia=resumen.ganancia,
    comision=resumen.comision,
    impuestosCliente=resumen.impuestosCliente,
    impuestosProveedor=resumen.impuestosProveedor,
    abono=resumen.abono,
    descuentos=resumen.descuentos
)

    for det in resumen.detalles:
        detalle = DetalleResumen(
            pedido=det.pedido,
            cliente=det.cliente,
            venta=det.venta,
            costo=det.costo,
            envio=det.envio
        )
        res_db.detalles.append(detalle)
    db.add(res_db)
    db.commit()
    db.refresh(res_db)
    return {"message": "Resumen guardado correctamente"}

@router.put("/resumenes/{resumen_id}")
def editar_resumen(resumen_id: int, resumen: ResumenSchema, db: Session = Depends(get_db)):
    res_db = db.query(Resumen).filter(Resumen.id == resumen_id).first()
    if not res_db:
        raise HTTPException(status_code=404, detail="Resumen no encontrado")
    
    res_db.fecha = resumen.fecha
    res_db.total_ventas = resumen.totalVentas
    res_db.total_costos = resumen.totalCostos
    res_db.ganancia = resumen.ganancia
    res_db.comision = resumen.comision
    res_db.impuestos_cliente = resumen.impuestosCliente
    res_db.impuestos_proveedor = resumen.impuestosProveedor
    res_db.abono = resumen.abono
    res_db.descuentos = resumen.descuentos

    res_db.detalles.clear()
    for det in resumen.detalles:
        detalle = DetalleResumen(
            pedido=det.pedido,
            cliente=det.cliente,
            venta=det.venta,
            costo=det.costo,
            envio=det.envio
        )
        res_db.detalles.append(detalle)

    db.commit()
    db.refresh(res_db)
    return {"message": "Resumen actualizado correctamente"}

@router.delete("/resumenes/{resumen_id}")
def eliminar_resumen(resumen_id: int, db: Session = Depends(get_db)):
    res_db = db.query(Resumen).filter(Resumen.id == resumen_id).first()
    if not res_db:
        raise HTTPException(status_code=404, detail="Resumen no encontrado")
    
    db.delete(res_db)
    db.commit()
    return {"message": "Resumen eliminado correctamente"}
