import random
import time

import nonebot
from nonebot import on_command, require
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import GroupMessageEvent
from nonebot.adapters.cqhttp.message import MessageSegment
from nonebot.typing import T_State

scheduler = require('nonebot_plugin_apscheduler').scheduler
master = nonebot.get_driver().config.master

class RPBot:
    def __init__(self):
        self.rp = {}

    def RP(self,num):
        if num in self.rp.keys():
            return self.rp[num]
        else:
            if num in master:
                self.rp[num] = random.randrange(51) + 50
            else:
                self.rp[num] = random.randrange(101)
            return self.rp[num]

rpbot = RPBot()

jrrp = on_command('jrrp')
@jrrp.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    if str(event.raw_message) == 'jrrp':
        user_id = event.user_id
        jp = rpbot.RP(user_id)
        msg= f'今天的人品值是:{jp}'
        await bot.send(event, message=MessageSegment.at(user_id)+msg)
        
@scheduler.scheduled_job('cron', hour='0', minute='0', second='0', misfire_grace_time=60) # = UTC+8 1445
async def clean():
    rpbot.rp = {}

