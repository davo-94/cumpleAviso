"""
database.py — Configuración de la conexión a la base de datos.

En desarrollo usa SQLite (archivo local cumpleaviso.db).
En producción (Railway) usa PostgreSQL a través de la variable DATABASE_URL.
"""
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

_url = os.getenv("DATABASE_URL", "sqlite:///./cumpleaviso.db")

# Railway entrega la URL con prefijo "postgres://" (legado),
# pero SQLAlchemy 2.x requiere "postgresql://". Se corrige aquí.
if _url.startswith("postgres://"):
    _url = _url.replace("postgres://", "postgresql://", 1)

# SQLite necesita check_same_thread=False para funcionar con FastAPI (multithreading).
# PostgreSQL no tiene esa restricción.
_connect_args = {"check_same_thread": False} if _url.startswith("sqlite") else {}

engine = create_engine(_url, connect_args=_connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    """
    Dependencia de FastAPI que provee una sesión de BD por request.
    Garantiza que la sesión se cierre al finalizar, incluso si hay errores.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
