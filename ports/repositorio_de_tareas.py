# ports/repositorio_de_tareas.py
# Define el puerto de salida (interface) para almacenar tareas. El núcleo usará esta interfaz sin saber cómo está implementada.

from abc import ABC, abstractmethod
from domain.tarea import Tarea
from typing import List

class RepositorioDeTareas(ABC):
    @abstractmethod
    def guardar(self, tarea: Tarea) -> None:
        pass

    @abstractmethod
    def obtener_todas(self) -> List[Tarea]:
        pass
