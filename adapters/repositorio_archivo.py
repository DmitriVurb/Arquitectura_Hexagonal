# Este adaptador usará un archivo llamado tareas.txt para guardar las tareas una por línea.
# adapters/repositorio_archivo.py

from ports.repositorio_de_tareas import RepositorioDeTareas
from domain.tarea import Tarea
from typing import List
from datetime import datetime
import os

class RepositorioEnArchivo(RepositorioDeTareas):
    def __init__(self, ruta_archivo="tareas.txt"):
        self.ruta = ruta_archivo

    def guardar(self, tarea: Tarea) -> None:
        with open(self.ruta, "a", encoding="utf-8") as f:
            linea = f"{tarea.titulo}|{int(tarea.completada)}|{tarea.fecha_creacion.isoformat()}\n"
            f.write(linea)

    def obtener_todas(self) -> List[Tarea]:
        if not os.path.exists(self.ruta):
            return []

        tareas = []
        with open(self.ruta, "r", encoding="utf-8") as f:
            for linea in f:
                partes = linea.strip().split("|")
                if len(partes) == 3:
                    titulo, completada_str, fecha_str = partes
                    tarea = Tarea(
                        titulo=titulo,
                        completada=bool(int(completada_str)),
                        fecha_creacion=datetime.fromisoformat(fecha_str)
                    )
                    tareas.append(tarea)
        return tareas
