# Tareas Hexagonal con FastAPI

Este proyecto implementa una arquitectura hexagonal (puertos y adaptadores) usando Python y FastAPI para la gestión de tareas.

## Características

- Puedes listar y crear tareas mediante consola o API (Swagger).
- Prueba distintos adaptadores de persistencia: en memoria, archivo o SQLite.
- El core de negocio es independiente del mecanismo de almacenamiento.

## Cómo ejecutar

```bash
python main.py
```

Si se desea ejecutar sin consola (presionando "n"), usar la siguiente URL:

