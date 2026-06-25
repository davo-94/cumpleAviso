"""
schemas.py — Schemas Pydantic para validación de entrada y serialización de salida.

FastAPI usa estos schemas para:
  - Validar automáticamente el cuerpo de las peticiones (ColaboradorCreate)
  - Serializar las respuestas de la API (ColaboradorOut, EnvioRegaliaOut, etc.)
"""
from pydantic import BaseModel, EmailStr, field_validator, ConfigDict
from datetime import date, datetime
from typing import Literal, Optional


class ColaboradorCreate(BaseModel):
    """Schema para crear un colaborador. Valida formato y restricciones de negocio."""
    nombre: str
    email: EmailStr                              # Pydantic valida el formato de email
    fec_nac: date
    regalo_pref: Literal["cine", "spa", "libro"] # Solo acepta estos tres valores exactos
    avisar_empresa: bool = False
    area: Optional[str] = None
    fec_ingreso: Optional[date] = None

    @field_validator("fec_nac")
    @classmethod
    def fecha_nac_no_futura(cls, v: date) -> date:
        """Un colaborador no puede nacer hoy ni en el futuro."""
        if v >= date.today():
            raise ValueError("La fecha de nacimiento no puede ser futura o de hoy")
        return v

    @field_validator("fec_ingreso")
    @classmethod
    def fecha_ingreso_no_futura(cls, v: Optional[date]) -> Optional[date]:
        """La fecha de ingreso no puede ser futura (campo opcional)."""
        if v and v > date.today():
            raise ValueError("La fecha de ingreso no puede ser futura")
        return v


class ColaboradorOut(BaseModel):
    """
    Schema de respuesta para colaboradores.
    from_attributes=True permite construirlo directamente desde un modelo SQLAlchemy.
    """
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    email: str
    fec_nac: date
    regalo_pref: str
    activo: bool
    avisar_empresa: bool
    foto: Optional[str] = None
    area: Optional[str] = None
    fec_ingreso: Optional[date] = None


class EnvioRegaliaOut(BaseModel):
    """Schema de respuesta para el historial de envíos de regalías."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    id_colab: int
    nombre_colab: str
    email_colab: str
    fecha: datetime
    codigo: str
    estado_envio: str


class LogEjecucionOut(BaseModel):
    """Schema de respuesta para el historial de ejecuciones del job."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    fecha: datetime
    resultado: str
    cantidad_encontrados: int
    detalle: Optional[str]
