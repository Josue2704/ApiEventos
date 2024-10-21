from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Evento

router = APIRouter()

@router.get("/")
def leer_eventos(db: Session = Depends(get_db)):
    print("Endpoint /eventos/ llamado")
    eventos = db.query(Evento).all()
    return eventos


@router.post("/")
def crear_evento(nombre: str, fecha: str, hora: str, ubicacion: str, db: Session = Depends(get_db)):
    evento = Evento(nombre=nombre, fecha=fecha, hora=hora, ubicacion=ubicacion)
    db.add(evento)
    db.commit()
    db.refresh(evento)
    return evento
