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

Base.metadata.create_all(bind=engine)

# Migración ligera: agrega columna foto si la DB ya existía sin ella
with engine.connect() as _conn:
    try:
        _conn.execute(text("ALTER TABLE colaboradores ADD COLUMN foto VARCHAR"))
        _conn.commit()
    except Exception:
        pass  # columna ya existe

FRONTEND = Path(__file__).parent.parent.parent / "frontend" / "dist"
UPLOADS = Path(__file__).parent.parent / "uploads"
UPLOADS.mkdir(exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()
    yield
    stop_scheduler()


app = FastAPI(title="CumpleAviso", description="Sistema de avisos de cumpleanos", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(colaboradores.router)
app.include_router(envios.router)

app.mount("/uploads", StaticFiles(directory=str(UPLOADS)), name="uploads")

# Sirve los assets compilados por Vite (JS/CSS con hash)
if FRONTEND.exists() and (FRONTEND / "assets").exists():
    app.mount("/assets", StaticFiles(directory=str(FRONTEND / "assets")), name="frontend_assets")


@app.get("/favicon.svg")
def favicon():
    f = FRONTEND / "favicon.svg"
    return FileResponse(f) if f.exists() else JSONResponse({"detail": "not found"}, status_code=404)


@app.get("/")
def root():
    index = FRONTEND / "index.html"
    if index.exists():
        return FileResponse(index)
    return JSONResponse({"message": "API ejecutándose. Compila el frontend: cd frontend && npm install && npm run build"})


# SPA fallback: cualquier ruta no-API devuelve index.html para el enrutamiento del cliente
@app.get("/{full_path:path}")
def spa_fallback(full_path: str):
    index = FRONTEND / "index.html"
    if index.exists():
        return FileResponse(index)
    return JSONResponse({"detail": "Not found"}, status_code=404)
