from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlmodel import Session
from app.core.database import engine
from app.services.sync_service import get_active_provider, run_sync

scheduler = AsyncIOScheduler()


def run_sync_job():
    """Fetch active provider/config and run sync in a DB session."""
    with Session(engine) as db:
        provider = get_active_provider(db)
        if not provider:
            return

        run_sync(db, provider)


def start_scheduler():
    """Start the scheduler."""
    # trigger = CronTrigger(minute="*")
    trigger = CronTrigger(minute="0", hour="*/2")

    scheduler.add_job(
        run_sync_job,
        trigger=trigger,
        id="hris_sync_job",
        replace_existing=True,
    )
    scheduler.start()
