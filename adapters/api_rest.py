# adapters/api_rest.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

from ports.servicio_tareas import ServicioDeTareas
from adapters.repositorio_sqlite import RepositorioSQLite
from domain.tarea import Tarea

app = FastAPI()
servicio = ServicioDeTareas(RepositorioSQLite())  # Puedes cambiar al adaptador que quieras

# DTO para entrada
class TareaInput(BaseModel):
    titulo: str

# DTO para salida
class TareaOutput(BaseModel):
    titulo: str
    completada: bool
    fecha_creacion: str

@app.post("/tareas")
def crear_tarea(tarea: TareaInput):
    try:
        servicio.crear_tarea(tarea.titulo)
        return {"mensaje": "Tarea creada correctamente"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/tareas", response_model=List[TareaOutput])
def listar_tareas():
    tareas = servicio.listar_tareas()
    return [
        TareaOutput(
            titulo=t.titulo,
            completada=t.completada,
            fecha_creacion=t.fecha_creacion.isoformat()
        )
        for t in tareas
    ]
