from pydantic import BaseModel, EmailStr, field_validator, ConfigDict
from datetime import date, datetime
from typing import Literal, Optional


class ColaboradorCreate(BaseModel):
    nombre: str
    email: EmailStr
    fec_nac: date
    regalo_pref: Literal["cine", "spa", "libro"]
    avisar_empresa: bool = False

    @field_validator("fec_nac")
    @classmethod
    def fecha_no_futura(cls, v: date) -> date:
        if v >= date.today():
            raise ValueError("La fecha de nacimiento no puede ser futura o de hoy")
        return v


class ColaboradorOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    email: str
    fec_nac: date
    regalo_pref: str
    activo: bool
    avisar_empresa: bool
    foto: Optional[str] = None


class EnvioRegaliaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    id_colab: int
    nombre_colab: str
    email_colab: str
    fecha: datetime
    codigo: str
    estado_envio: str


class LogEjecucionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    fecha: datetime
    resultado: str
    cantidad_encontrados: int
    detalle: Optional[str]
