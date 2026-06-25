"""
models.py — Modelos ORM que representan las tablas de la base de datos.

SQLAlchemy mapea cada clase a una tabla y cada atributo a una columna.
Al importar este módulo y llamar Base.metadata.create_all(), las tablas
se crean automáticamente si no existen.
"""
from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, Text
from sqlalchemy.sql import func
from .database import Base


class Colaborador(Base):
    """
    Tabla principal. Almacena los datos de cada colaborador de la empresa.
    El campo 'activo' controla si el colaborador recibe notificaciones.
    El campo 'avisar_empresa' controla si se notifica a RR.HH. en su cumpleaños.
    """
    __tablename__ = "colaboradores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    fec_nac = Column(Date, nullable=False)
    regalo_pref = Column(String, nullable=False)  # cine | spa | libro
    activo = Column(Boolean, default=True)
    avisar_empresa = Column(Boolean, default=False)
    foto = Column(String, nullable=True)           # nombre del archivo en /uploads
    area = Column(String, nullable=True)
    fec_ingreso = Column(Date, nullable=True)
    created_at = Column(DateTime, server_default=func.now())


class LogEjecucion(Base):
    """
    Historial de ejecuciones del job diario.
    Cada vez que el job corre (automático o manual) se registra un log.
    """
    __tablename__ = "logs_ejecucion"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime, server_default=func.now())
    resultado = Column(String)           # ok | error
    cantidad_encontrados = Column(Integer, default=0)
    detalle = Column(Text, nullable=True)


class EnvioRegalia(Base):
    """
    Registro de cada correo de regalo enviado a un colaborador.
    Incluye el código de canje generado y el estado del envío.
    """
    __tablename__ = "envios_regalias"

    id = Column(Integer, primary_key=True, index=True)
    id_colab = Column(Integer, nullable=False)
    nombre_colab = Column(String)
    email_colab = Column(String)
    fecha = Column(DateTime, server_default=func.now())
    codigo = Column(String)
    estado_envio = Column(String, default="pendiente")  # enviado | fallido


class EnvioEmpresa(Base):
    """
    Registro de notificaciones enviadas al email corporativo (RR.HH.).
    Incluye tanto los avisos de cumpleaños como los recordatorios anticipados.
    """
    __tablename__ = "envios_empresa"

    id = Column(Integer, primary_key=True, index=True)
    id_colab = Column(Integer, nullable=False)
    nombre_colab = Column(String)
    fecha = Column(DateTime, server_default=func.now())
    destinatario = Column(String)
    exito = Column(Boolean, default=False)
    tipo = Column(String, default="cumpleanos")  # cumpleanos | recordatorio
