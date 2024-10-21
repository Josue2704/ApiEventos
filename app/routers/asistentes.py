from typing import List, Optional
import qrcode
from io import BytesIO
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models import Asistente, AsistenteORM

router = APIRouter()

# Modelo para recibir los datos en el body como JSON
class AsistenteCreate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[str]= None
    evento_id: Optional[int] = None

# Registrar asistente y generar QR como PNG
@router.post("/", status_code=status.HTTP_201_CREATED)
async def registrar_asistente(
    asistente: AsistenteCreate, db: Session = Depends(get_db)
):

    print(f"Datos recibidos: {asistente}")
    # Crear asistente en la base de datos
    nuevo_asistente = AsistenteORM(
        nombre=asistente.nombre,
        email=asistente.email,
        evento_id=asistente.evento_id,
        presente=False
    )
    db.add(nuevo_asistente)
    db.commit()
    db.refresh(nuevo_asistente)

    # Generar QR con el ID del asistente para la validación
    qr_data = f"http://localhost:8003/asistentes/validar/{nuevo_asistente.id}"
    qr = qrcode.make(qr_data)

    # Guardar el QR en memoria como PNG
    buf = BytesIO()
    qr.save(buf, format="PNG")
    buf.seek(0)  # Reiniciar el puntero del buffer

    # Devolver la imagen PNG directamente como respuesta
    return Response(content=buf.getvalue(), media_type="image/png")


# Validar asistente y marcar como presente
@router.get("/validar/{asistente_id}")
def validar_asistencia(asistente_id: int, db: Session = Depends(get_db)):
    # Buscar al asistente por ID
    asistente = db.query(AsistenteORM).filter(AsistenteORM.id == asistente_id).first()

    if not asistente:
        raise HTTPException(status_code=404, detail="Asistente no encontrado")

    if asistente.presente:
        raise HTTPException(
            status_code=400, detail="El asistente ya está marcado como presente"
        )

    # Marcar como presente y guardar en la base de datos
    asistente.presente = True
    db.commit()

    return {"detail": f"Asistencia del asistente {asistente.nombre} validada"}

# Obtener todos los asistentes (con modelo ORM)
@router.get("/asistentes/", response_model=List[Asistente])
def obtener_asistentes(db: Session = Depends(get_db)):
    asistentes = db.query(AsistenteORM).all()
    if not asistentes:
        raise HTTPException(status_code=404, detail="No hay asistentes registrados")
    return asistentes

# Obtener un asistente por ID
@router.get("/{asistente_id}", response_model=Asistente)
def obtener_asistente(asistente_id: int, db: Session = Depends(get_db)):
    asistente = db.query(AsistenteORM).filter(AsistenteORM.id == asistente_id).first()
    if not asistente:
        raise HTTPException(status_code=404, detail="Asistente no encontrado")
    return asistente
