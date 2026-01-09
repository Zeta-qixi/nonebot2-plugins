
from .model import Clock
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler


class SchedulerAdapter:
    def __init__(self, scheduler: AsyncIOScheduler):
        self.scheduler =  scheduler

    def add(self, clock: Clock, callback):
        trigger = CronTrigger.from_crontab(clock.cron_expression)
        self.scheduler.add_job(
            callback,
            trigger=trigger,
            id=f"clock_{clock.id}",
            args=[clock],
            misfire_grace_time=60,
            coalesce=False
        )

    def remove(self, clock_id: int):
        try:
            self.scheduler.remove_job(f"clock_{clock_id}")
        except Exception:
            pass



