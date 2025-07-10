# adapters/repositorio_memoria.py

from ports.repositorio_de_tareas import RepositorioDeTareas
from domain.tarea import Tarea
from typing import List

class RepositorioEnMemoria(RepositorioDeTareas):
    def __init__(self):
        self._tareas: List[Tarea] = []

    def guardar(self, tarea: Tarea) -> None:
        self._tareas.append(tarea)

    def obtener_todas(self) -> List[Tarea]:
        return self._tareas
