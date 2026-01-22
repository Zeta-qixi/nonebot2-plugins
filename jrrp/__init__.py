
import nonebot
import time
import re
import random
from nonebot import on_command, require
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from nonebot.adapters.onebot.v11.message import MessageSegment, Message
from nonebot.params import  CommandArg


from nonebot import require
simple_chat = require('nonebot_plugin_anywhere_llm').simple_chat


def fortune_level(score: int) -> str:
    levels = [
        (15, "大凶"),
        (30, "凶"),
        (50, "小凶"),
        (65, "末吉"),
        (80, "小吉"),
        (90, "吉"),
        (100, "大吉")
    ]

    for threshold, level in levels:
        if score <= threshold:
            return level


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
            
            response = await simple_chat(
                workspace_name="jrrp", 
                prompt=f"抽签: {fortune_level(rp)}",
            )
            if response:
                for r in re.split(r'[\\\n$]', response):
                    r=r.strip()
                    if r:
                        time.sleep(len(r) / 12 * random.randint(1,3))
                        await matcher.send(r)
    


@scheduler.scheduled_job('cron', hour='0', minute='0', second='0', misfire_grace_time=60) # = UTC+8 1445
async def clean():
    global Jrrp
    Jrrp = {}

