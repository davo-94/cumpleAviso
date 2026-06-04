from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from .services.birthday_job import run_birthday_job

_scheduler = BackgroundScheduler()


def start_scheduler():
    _scheduler.add_job(
        run_birthday_job,
        CronTrigger(hour=6, minute=0),
        id="birthday_job",
        name="Job diario cumpleanos",
        replace_existing=True,
    )
    _scheduler.start()
    print("[SCHEDULER] Iniciado — job diario a las 06:00")


def stop_scheduler():
    if _scheduler.running:
        _scheduler.shutdown()
