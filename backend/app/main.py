"""
main.py — Punto de entrada de la aplicación FastAPI.

Responsabilidades:
  1. Crear las tablas en BD al arrancar (create_all)
  2. Ejecutar migraciones ligeras para columnas agregadas después del deploy inicial
  3. Sembrar datos de prueba si la BD está vacía (seed_db)
  4. Registrar los routers de la API
  5. Servir el frontend React compilado como archivos estáticos
  6. Implementar el fallback SPA para que las rutas del cliente funcionen al recargar
"""
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text

from .database import engine, Base
from .routers import colaboradores, envios
from .scheduler import start_scheduler, stop_scheduler

# Crea todas las tablas definidas en models.py si no existen todavía
Base.metadata.create_all(bind=engine)

# Migraciones ligeras: agrega columnas que no existían en el schema original.
# Cada migración usa su propia conexión porque PostgreSQL aborta toda la transacción
# al encontrar un error (ej: columna ya existe). Con una conexión compartida,
# una migración fallida dejaría las siguientes sin ejecutarse.
_MIGRATIONS = [
    "ALTER TABLE colaboradores ADD COLUMN foto VARCHAR",
    "ALTER TABLE colaboradores ADD COLUMN area VARCHAR",
    "ALTER TABLE colaboradores ADD COLUMN fec_ingreso DATE",
]
for _sql in _MIGRATIONS:
    with engine.connect() as _conn:
        try:
            _conn.execute(text(_sql))
            _conn.commit()
        except Exception:
            pass  # columna ya existe, se ignora el error

# Ruta al bundle compilado de React/Vite.
# En desarrollo esta carpeta no existe; el frontend corre en su propio dev server.
# En producción (Railway) se genera con `npm run build` antes del deploy.
FRONTEND = Path(__file__).parent.parent.parent / "frontend" / "dist"
UPLOADS = Path(__file__).parent.parent / "uploads"
UPLOADS.mkdir(exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Hook de ciclo de vida de FastAPI.
    Al arrancar: siembra datos de prueba y activa el scheduler.
    Al apagar: detiene el scheduler limpiamente.
    """
    from .seed import seed_db
    seed_db()
    start_scheduler()
    yield
    stop_scheduler()


app = FastAPI(title="CumpleAviso", description="Sistema de avisos de cumpleanos", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # En producción se puede restringir al dominio de Vercel
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(colaboradores.router)
app.include_router(envios.router)

# Archivos subidos por usuarios (fotos de perfil)
app.mount("/uploads", StaticFiles(directory=str(UPLOADS)), name="uploads")

# Assets compilados de Vite (JS/CSS con hash de contenido para cache-busting)
if FRONTEND.exists() and (FRONTEND / "assets").exists():
    app.mount("/assets", StaticFiles(directory=str(FRONTEND / "assets")), name="frontend_assets")


@app.get("/favicon.svg")
def favicon():
    f = FRONTEND / "favicon.svg"
    return FileResponse(f) if f.exists() else JSONResponse({"detail": "not found"}, status_code=404)


@app.get("/")
def root():
    """Sirve el index.html del frontend o un mensaje de estado si no está compilado."""
    index = FRONTEND / "index.html"
    if index.exists():
        return FileResponse(index)
    return JSONResponse({"message": "API ejecutándose. Compila el frontend: cd frontend && npm install && npm run build"})


@app.get("/{full_path:path}")
def spa_fallback(full_path: str):
    """
    Fallback para el enrutamiento de la SPA de React.
    Cualquier ruta que no coincida con un endpoint de la API devuelve index.html,
    permitiendo que React Router maneje la navegación en el cliente.
    Sin esto, recargar la página en una ruta que no sea '/' daría un 404.
    """
    index = FRONTEND / "index.html"
    if index.exists():
        return FileResponse(index)
    return JSONResponse({"detail": "Not found"}, status_code=404)
