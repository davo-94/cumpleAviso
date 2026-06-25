"""
routers/envios.py — Endpoints para historial de envíos, logs y ejecución manual del job.

El endpoint /api/jobs/ejecutar permite disparar el job de cumpleaños manualmente,
lo que es útil para pruebas o para forzar el reenvío sin esperar al cron de las 06:00.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from ..auth import require_auth
from ..database import get_db
from ..models import EnvioRegalia, LogEjecucion
from ..schemas import EnvioRegaliaOut, LogEjecucionOut
from ..services.birthday_job import run_birthday_job

router = APIRouter(prefix="/api", tags=["envios"])


@router.get("/envios", response_model=List[EnvioRegaliaOut])
def listar_envios(db: Session = Depends(get_db), _: str = Depends(require_auth)):
    """Devuelve los últimos 50 envíos de regalías ordenados por fecha descendente."""
    return (
        db.query(EnvioRegalia)
        .order_by(EnvioRegalia.fecha.desc())
        .limit(50)
        .all()
    )


@router.get("/logs", response_model=List[LogEjecucionOut])
def listar_logs(db: Session = Depends(get_db), _: str = Depends(require_auth)):
    """Devuelve las últimas 20 ejecuciones del job ordenadas por fecha descendente."""
    return (
        db.query(LogEjecucion)
        .order_by(LogEjecucion.fecha.desc())
        .limit(20)
        .all()
    )


@router.post("/jobs/ejecutar")
def ejecutar_job_manual(_: str = Depends(require_auth)):
    """Disparador manual del job de cumpleanos (para pruebas)."""
    run_birthday_job()
    return {"message": "Job ejecutado correctamente"}
