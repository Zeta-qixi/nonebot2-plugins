
import nonebot
import random
from nonebot import on_command, require
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from nonebot.adapters.onebot.v11.message import MessageSegment, Message
from nonebot.params import  CommandArg
from .llm import llm_respone

Jrrp = {}
scheduler = require('nonebot_plugin_apscheduler').scheduler
master = nonebot.get_driver().config.master
jrrp = on_command('jrrp',block=True)

@jrrp.handle()
async def jrrp_(matcher: Matcher, event: GroupMessageEvent):
        if  rp:=Jrrp.get(event.user_id):
            await matcher.finish( message=MessageSegment.at(event.user_id) + f'今日的人品值是:{rp}')
        else:
            rp = random.randint(0, 100)
            Jrrp[event.user_id] = rp
            await matcher.send( message=MessageSegment.at(event.user_id) + f'今日的人品值是:{rp}')
            
            respone = await llm_respone(rp)
            await matcher.finish( message=respone)


@scheduler.scheduled_job('cron', hour='0', minute='0', second='0', misfire_grace_time=60) # = UTC+8 1445
async def clean():
    Game.clear()

