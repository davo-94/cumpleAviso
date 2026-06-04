from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import EnvioRegalia, LogEjecucion
from ..schemas import EnvioRegaliaOut, LogEjecucionOut
from ..services.birthday_job import run_birthday_job

router = APIRouter(prefix="/api", tags=["envios"])


@router.get("/envios", response_model=List[EnvioRegaliaOut])
def listar_envios(db: Session = Depends(get_db)):
    return (
        db.query(EnvioRegalia)
        .order_by(EnvioRegalia.fecha.desc())
        .limit(50)
        .all()
    )


@router.get("/logs", response_model=List[LogEjecucionOut])
def listar_logs(db: Session = Depends(get_db)):
    return (
        db.query(LogEjecucion)
        .order_by(LogEjecucion.fecha.desc())
        .limit(20)
        .all()
    )


@router.post("/jobs/ejecutar")
def ejecutar_job_manual():
    """Disparador manual del job de cumpleanos (para pruebas)."""
    run_birthday_job()
    return {"message": "Job ejecutado correctamente"}
