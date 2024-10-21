from fastapi import FastAPI
from app.routers import eventos, asistentes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Incluir los routers
app.include_router(eventos.router, prefix="/eventos", tags=["Eventos"])
app.include_router(asistentes.router, prefix="/asistentes", tags=["Asistentes"])



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas las fuentes
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos
    allow_headers=["*"],  # Permite todos los headers
)

@app.get("/")
def read_root():
    return {"message": "API funcionando"}


