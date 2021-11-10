import os
import time
import random
from .utils import *
from nonebot import on_command, on_regex

from nonebot.typing import T_State
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import Event


week_day = on_regex('(.*)是?(星期|周)几', block=False)
@week_day.handle()
async def recall_setu_handle(bot: Bot, event: Event, state: T_State):
    date, name_ = state['_matched_groups']
    try:
        msg = f"是{name_}{get_weekday(date)}{random.choice(['哦', '喔', ''])}~"
        await bot.send(event, message = msg)
    except ValueError:
        print('----')
        await bot.send(event, message = random.choice(['是你妈的祭日，傻狗', '?', f'{date}你玛呢']))


day = on_regex('(今天)是?几号', block=False)
@day.handle()
async def recall_setu_handle(bot: Bot, event: Event, state: T_State):
    date = datetime.date.today().__format__("%m.%d")
    msg = f"今天是{date}{random.choice(['哦', '喔', ''])}~"
    await bot.send(event, message = msg)