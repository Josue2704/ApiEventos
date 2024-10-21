from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

# Base para SQLAlchemy
Base = declarative_base()


# Modelo SQLAlchemy para la tabla Evento
class Evento(Base):
    __tablename__ = "eventos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    fecha = Column(String(10), nullable=False)
    hora = Column(String(8), nullable=False)
    ubicacion = Column(String(255), nullable=False)


# Modelo SQLAlchemy para la tabla Asistente
class AsistenteORM(Base):
    __tablename__ = "asistentes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    evento_id = Column(Integer, ForeignKey("eventos.id"), nullable=False)
    presente = Column(Boolean, default=False)


# Modelo Pydantic para la respuesta de Asistente
class Asistente(BaseModel):
    id: int
    nombre: str
    email: str
    presente: bool

    class Config:
        from_attributes = True  # Habilita la conversión de SQLAlchemy a Pydantic
