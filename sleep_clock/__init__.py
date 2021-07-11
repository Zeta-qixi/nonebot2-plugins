from nonebot import on_command, on_message, on_notice, get_bots
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import (Event, GroupMessageEvent,
                                           MessageEvent)
from nonebot.adapters.cqhttp.message import Message, MessageSegment
from nonebot.typing import T_State
from nonebot import require
from os import path, listdir
import time
import random
scheduler = require('nonebot_plugin_apscheduler').scheduler




path =path.abspath(__file__).split('__')[0]
img_src = path + '/data/sleep.png'
sleep_img = MessageSegment.image(f'file://{img_src}')

@scheduler.scheduled_job('cron', hour='23',minute='0', misfire_grace_time=60) # = UTC+8 1445
async def sleep():
    for bot in get_bots().values():
        for group in groups:
            await bot.send_group_msg(group_id=group,message=sleep_img)

def get_time():
    now = (time.strftime("%H:%M", time.localtime()))
    h = int(now[:2])
    m = int(now[3:])
    return (h,m)

sleep = on_command('睡觉')
@sleep.handle()
async def _(bot: Bot, event: Event, state: T_State):
    h, _ = get_time()
    if h >= 21 or h <= 2:
    
        list = listdir(path+'/data/sleep')
    
        img_src = path + f'/data/sleep/{random.choice(list)}'
        img = MessageSegment.image(f'file://{img_src}')
        await bot.send(event, message = img)
