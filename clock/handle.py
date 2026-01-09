from nonebot import require, get_driver
from .model import Clock
from .scheduler import SchedulerAdapter
from .database.database import ClockDB
from .utils import db_to_message
from .config import clock_config
scheduler = require('nonebot_plugin_apscheduler').scheduler
from nonebot.adapters.onebot.v11 import Bot, MessageSegment


class JobHandle:
    def __init__(self, db: ClockDB, scheduler: SchedulerAdapter, callback):
        self.db = db
        self.scheduler = scheduler
        self.callback = callback
        self._load_all()

    

    async def _wrap_callback(self, clock: Clock):
        """
        用于注入self
        """
        await self.callback(clock, self)


    def _load_all(self):
        for clock in self.db.select_all():
            if clock.is_enabled:
                self.scheduler.add(clock, self._wrap_callback)

    def add_clock(self, clock: Clock):
        clock.id = self.db.add(clock)
        if clock.is_enabled:
            self.scheduler.add(clock, self._wrap_callback)
        return clock.id

    def delete_clock(self, clock: Clock):
        self.scheduler.remove(clock.id)
        self.db.delete(clock.id)

    def enabled_clock(self, clock: Clock):
        if not clock.is_enabled:
            clock.is_enabled = True
            self.db.update(clock)
            self.scheduler.add(clock, self._wrap_callback)
            
            
    def disable_clock(self, clock: Clock):
        if clock.is_enabled:
            clock.is_enabled = False
            self.db.update(clock)
            self.scheduler.remove(clock.id)
       

    def list_clock(self, uid, gid):
        return self.db.select_by_owner(uid, gid)



async def callback(clock: Clock, handle: JobHandle):

    bots = get_driver().bots
    if not bots:
        return
    bot: Bot = list(bots.values())[0] 

    message = await db_to_message(clock.content)
    if clock.type == "private":
        await bot.send_msg(message_type="private",
                           user_id=clock.user_id,message=message)
    elif clock.type == "group":
        if clock_config.group_at_me:
            message = MessageSegment.at(clock.user_id) + message
        await bot.send_msg(
            message_type="group",
            group_id=clock.group_id, message=message,)
        
    if clock.is_one_time:
        handle.delete_clock(clock)


job_handle = JobHandle(
    db = ClockDB(db_path=clock_config.db_path),
    scheduler = SchedulerAdapter(scheduler),
    callback = callback
)