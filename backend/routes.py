from fastapi import APIRouter, Depends, Query
from backend.serialReaderService import leer_peso_automatico, obtener_total_registros_fecha

from database.database import get_db
from sqlalchemy.orm import Session

backend_router = APIRouter()


@backend_router.get("/peso")
def leer_peso_funcional(db: Session = Depends(get_db)):
    data = leer_peso_automatico(db)
    return data

@backend_router.get("/pesoPorFecha")
def leer_peso_funcional(fecha: str = Query(..., regex=r"^\d{4}-\d{2}-\d{2}$"), db: Session = Depends(get_db)):
    data = obtener_total_registros_fecha(fecha, db)
    return data
