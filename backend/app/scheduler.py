"""
scheduler.py — Configuración del scheduler en background.

Usa APScheduler con un trigger cron para ejecutar el job de cumpleaños
todos los días a las 06:00 AM (hora del servidor).

El scheduler corre en un hilo en background dentro del mismo proceso uvicorn.
Por esta razón el backend debe correr en Railway (proceso persistente),
no en Vercel (funciones serverless que no mantienen estado entre invocaciones).
"""
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from .services.birthday_job import run_birthday_job

_scheduler = BackgroundScheduler()


def start_scheduler():
    """Registra el job de cumpleaños y arranca el scheduler."""
    _scheduler.add_job(
        run_birthday_job,
        CronTrigger(hour=6, minute=0),
        id="birthday_job",
        name="Job diario cumpleanos",
        replace_existing=True,  # evita duplicados si el módulo se recarga
    )
    _scheduler.start()
    print("[SCHEDULER] Iniciado — job diario a las 06:00")


def stop_scheduler():
    """Detiene el scheduler limpiamente al apagar la aplicación."""
    if _scheduler.running:
        _scheduler.shutdown()
