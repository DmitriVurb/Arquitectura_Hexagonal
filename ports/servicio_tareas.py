# Representa la intención del negocio, como “crear una tarea” o “marcar como completada”. Llama al repositorio para cumplir su objetivo, pero no sabe cómo está implementado.
# ports/servicio_tareas.py

from domain.tarea import Tarea
from ports.repositorio_de_tareas import RepositorioDeTareas

class ServicioDeTareas:
    def __init__(self, repositorio: RepositorioDeTareas):
        self.repositorio = repositorio

    def crear_tarea(self, titulo: str):
        if not titulo.strip():
            raise ValueError("El título no puede estar vacío.")
        tarea = Tarea(titulo=titulo.strip())
        self.repositorio.guardar(tarea)

    def listar_tareas(self):
        return self.repositorio.obtener_todas()


