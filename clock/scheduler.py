from nonebot import require, get_bot
from .model import Clock
from .handle.job import JobHandle, del_clock
from .database.database import db
from .utils import db_to_message
scheduler = require('nonebot_plugin_apscheduler').scheduler
class Myhandle(JobHandle):
    def __init__(self, db, scheduler):
        super().__init__(db, scheduler)
    async def _job_function(self, clock: Clock):
        message = await db_to_message(clock.content)
        if clock.type == 'private':
            await get_bot().send_msg(message_type=clock.type, user_id=clock.user_id, message=message)
        elif clock.type == 'group':
            # message = MessageSegment.at(clock.user_id) + message
            await get_bot().send_msg(message_type=clock.type, group_id=clock.group_id, message=message)
        if clock.is_one_time:
            del_clock(myhandle, clock)
myhandle = Myhandle(db, scheduler)