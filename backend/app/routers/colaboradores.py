"""
routers/colaboradores.py — Endpoints CRUD para la gestión de colaboradores.

Todos los endpoints requieren autenticación HTTP Basic (require_auth).
Las fotos se almacenan como archivos en la carpeta /uploads del servidor.
"""
import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from typing import List

from ..auth import require_auth
from ..database import get_db
from ..models import Colaborador
from ..schemas import ColaboradorCreate, ColaboradorOut

router = APIRouter(prefix="/api", tags=["colaboradores"])

UPLOADS_DIR = Path(__file__).parent.parent.parent / "uploads"
UPLOADS_DIR.mkdir(exist_ok=True)

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}


@router.post("/colaborador", response_model=ColaboradorOut, status_code=201)
def crear_colaborador(
    data: ColaboradorCreate,
    db: Session = Depends(get_db),
    _: str = Depends(require_auth),
):
    """
    Registra un nuevo colaborador en el sistema.
    Retorna 409 si el email ya existe (restricción unique en BD).
    FastAPI valida automáticamente el body contra ColaboradorCreate (422 si falla).
    """
    if db.query(Colaborador).filter(Colaborador.email == data.email).first():
        raise HTTPException(status_code=409, detail="Email ya registrado")
    colab = Colaborador(**data.model_dump())
    db.add(colab)
    db.commit()
    db.refresh(colab)
    return colab


@router.get("/colaboradores", response_model=List[ColaboradorOut])
def listar_colaboradores(
    db: Session = Depends(get_db),
    _: str = Depends(require_auth),
):
    """Devuelve todos los colaboradores ordenados del más reciente al más antiguo."""
    return db.query(Colaborador).order_by(Colaborador.id.desc()).all()


@router.patch("/colaborador/{colab_id}/inactivar")
def inactivar_colaborador(
    colab_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(require_auth),
):
    """
    Marca un colaborador como inactivo (activo=False).
    Los colaboradores inactivos no reciben notificaciones de cumpleaños.
    No se eliminan de la BD para mantener el historial de envíos.
    """
    colab = db.query(Colaborador).filter(Colaborador.id == colab_id).first()
    if not colab:
        raise HTTPException(status_code=404, detail="Colaborador no encontrado")
    colab.activo = False
    db.commit()
    return {"message": f"Colaborador '{colab.nombre}' deshabilitado"}


@router.post("/colaborador/{colab_id}/foto", response_model=ColaboradorOut)
async def subir_foto(
    colab_id: int,
    foto: UploadFile = File(...),
    db: Session = Depends(get_db),
    _: str = Depends(require_auth),
):
    """
    Sube o reemplaza la foto de perfil de un colaborador.
    El archivo se guarda en /uploads con nombre único (id + uuid) para evitar colisiones.
    Si ya existe una foto anterior, se elimina del disco.
    """
    colab = db.query(Colaborador).filter(Colaborador.id == colab_id).first()
    if not colab:
        raise HTTPException(status_code=404, detail="Colaborador no encontrado")
    if foto.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Solo se aceptan imagenes (jpg, png, gif, webp)")

    ext = foto.filename.rsplit(".", 1)[-1].lower() if "." in foto.filename else "jpg"
    filename = f"{colab_id}_{uuid.uuid4().hex[:8]}.{ext}"
    dest = UPLOADS_DIR / filename

    # Borrar foto anterior si existe para no acumular archivos huérfanos
    if colab.foto:
        old = UPLOADS_DIR / colab.foto
        if old.exists():
            old.unlink()

    content = await foto.read()
    dest.write_bytes(content)

    colab.foto = filename
    db.commit()
    db.refresh(colab)
    return colab
