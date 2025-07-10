# domain/tarea.py

from dataclasses import dataclass
from datetime import datetime

@dataclass
class Tarea:
    titulo: str
    fecha_creacion: datetime = datetime.now()
    completada: bool = False

    def marcar_completada(self):
        self.completada = True
