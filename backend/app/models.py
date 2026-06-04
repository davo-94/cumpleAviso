from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, Text
from sqlalchemy.sql import func
from .database import Base


class Colaborador(Base):
    __tablename__ = "colaboradores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    fec_nac = Column(Date, nullable=False)
    regalo_pref = Column(String, nullable=False)  # cine | spa | libro
    activo = Column(Boolean, default=True)
    avisar_empresa = Column(Boolean, default=False)
    foto = Column(String, nullable=True)
    area = Column(String, nullable=True)
    fec_ingreso = Column(Date, nullable=True)
    created_at = Column(DateTime, server_default=func.now())


class LogEjecucion(Base):
    __tablename__ = "logs_ejecucion"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime, server_default=func.now())
    resultado = Column(String)  # ok | error
    cantidad_encontrados = Column(Integer, default=0)
    detalle = Column(Text, nullable=True)


class EnvioRegalia(Base):
    __tablename__ = "envios_regalias"

    id = Column(Integer, primary_key=True, index=True)
    id_colab = Column(Integer, nullable=False)
    nombre_colab = Column(String)
    email_colab = Column(String)
    fecha = Column(DateTime, server_default=func.now())
    codigo = Column(String)
    estado_envio = Column(String, default="pendiente")  # enviado | fallido


class EnvioEmpresa(Base):
    __tablename__ = "envios_empresa"

    id = Column(Integer, primary_key=True, index=True)
    id_colab = Column(Integer, nullable=False)
    nombre_colab = Column(String)
    fecha = Column(DateTime, server_default=func.now())
    destinatario = Column(String)
    exito = Column(Boolean, default=False)
    tipo = Column(String, default="cumpleanos")  # cumpleanos | recordatorio
