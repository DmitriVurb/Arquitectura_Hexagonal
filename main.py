# main.py

from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from typing import List
from ports.servicio_tareas import ServicioDeTareas
from adapters.repositorio_memoria import RepositorioEnMemoria
from adapters.repositorio_archivo import RepositorioEnArchivo
from adapters.repositorio_sqlite import RepositorioSQLite
from datetime import datetime


# -------------------------------
# Modelos Pydantic
# -------------------------------
class TareaRequest(BaseModel):
    titulo: str

class TareaResponse(BaseModel):
    titulo: str
    completada: bool
    fecha_creacion: str  # ISO 8601


# -------------------------------
# Repositorio dinámico
# -------------------------------
def elegir_adaptador(tipo: str):
    if tipo == "memoria":
        return RepositorioEnMemoria()
    elif tipo == "archivo":
        return RepositorioEnArchivo("tareas.txt")
    elif tipo == "sqlite":
        return RepositorioSQLite("tareas.db")
    else:
        raise ValueError("Tipo de repositorio no válido. Usa: memoria, archivo o sqlite.")


# -------------------------------
# Modo consola
# -------------------------------
def menu_consola():
    tipo = input("Selecciona el tipo de repositorio (memoria / archivo / sqlite): ").lower()
    try:
        servicio = ServicioDeTareas(elegir_adaptador(tipo))
    except ValueError as e:
        print(f"⚠️ Error: {e}")
        return

    while True:
        print("\nOpciones:")
        print("1 - Crear tarea")
        print("2 - Listar tareas")
        print("3 - Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            titulo = input("Título de la tarea: ")
            try:
                servicio.crear_tarea(titulo)
                print("✅ Tarea creada.")
            except ValueError as e:
                print(f"⚠️ Error: {e}")

        elif opcion == "2":
            tareas = servicio.listar_tareas()
            if not tareas:
                print("📭 No hay tareas registradas.")
            else:
                print("\n📋 Lista de tareas:")
                for idx, tarea in enumerate(tareas, 1):
                    estado = "✅" if tarea.completada else "⏳"
                    print(f"{idx}. {tarea.titulo} [{estado}] - {tarea.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S')}")

        elif opcion == "3":
            print("👋 Saliendo...")
            break
        else:
            print("❌ Opción inválida.")


# -------------------------------
# API con FastAPI
# -------------------------------
app = FastAPI()

@app.post("/tareas", response_model=TareaResponse)
def crear_tarea(tarea: TareaRequest, tipo: str = Query("memoria", description="memoria / archivo / sqlite")):
    try:
        servicio = ServicioDeTareas(elegir_adaptador(tipo))
        nueva = servicio.crear_tarea(tarea.titulo)
        return TareaResponse(
            titulo=nueva.titulo,
            completada=nueva.completada,
            fecha_creacion=nueva.fecha_creacion.isoformat()
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/tareas", response_model=List[TareaResponse])
def listar_tareas(tipo: str = Query("memoria", description="memoria / archivo / sqlite")):
    try:
        servicio = ServicioDeTareas(elegir_adaptador(tipo))
        tareas = servicio.listar_tareas()
        return [
            TareaResponse(
                titulo=t.titulo,
                completada=t.completada,
                fecha_creacion=t.fecha_creacion.isoformat()
            ) for t in tareas
        ]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# -------------------------------
# Modo seleccionable
# -------------------------------
if __name__ == "__main__":
    modo = input("¿Modo consola? (s/n): ").lower()
    if modo == "s":
        menu_consola()
    else:
        import uvicorn
        uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
