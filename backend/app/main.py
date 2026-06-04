from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
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

FRONTEND = Path(__file__).parent.parent.parent / "frontend"
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
app.mount("/static", StaticFiles(directory=str(FRONTEND)), name="static")


@app.get("/")
def root():
    return FileResponse(FRONTEND / "index.html")
