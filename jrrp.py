from nonebot import on_command, on_message, on_notice
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import (Event, GroupMessageEvent,
                                           MessageEvent, PokeNotifyEvent)
from nonebot.adapters.cqhttp.message import Message, MessageSegment
from nonebot.typing import T_State
import time
import random
import nonebot
from nonebot import require

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
    msg = event.raw_message
    user_id = event.user_id
    jp = rpbot.RP(user_id)
    msg= f'今天的人品值是:{jp}'
    await bot.send(event, message=MessageSegment.at(user_id)+msg)
    
@scheduler.scheduled_job('cron', hour='0', minute='0', second='0', misfire_grace_time=60) # = UTC+8 1445
async def clean():
    rpbot.rp = {}

