# adapters/repositorio_sqlite.py

import sqlite3
from typing import List
from domain.tarea import Tarea
from ports.repositorio_de_tareas import RepositorioDeTareas
from datetime import datetime

class RepositorioSQLite(RepositorioDeTareas):
    def __init__(self, db_path="tareas.db"):
        self.conn = sqlite3.connect(db_path)
        self._crear_tabla()

    def _crear_tabla(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS tareas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    completada INTEGER NOT NULL,
                    fecha_creacion TEXT NOT NULL
                )
            """)

    def guardar(self, tarea: Tarea) -> None:
        with self.conn:
            self.conn.execute("""
                INSERT INTO tareas (titulo, completada, fecha_creacion)
                VALUES (?, ?, ?)
            """, (tarea.titulo, int(tarea.completada), tarea.fecha_creacion.isoformat()))

    def obtener_todas(self) -> List[Tarea]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT titulo, completada, fecha_creacion FROM tareas")
        filas = cursor.fetchall()

        tareas = []
        for titulo, completada, fecha_str in filas:
            tarea = Tarea(
                titulo=titulo,
                completada=bool(completada),
                fecha_creacion=datetime.fromisoformat(fecha_str)
            )
            tareas.append(tarea)
        return tareas
