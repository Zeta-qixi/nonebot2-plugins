import os
import time
import random
import datetime
import re
from nonebot import on_command, on_regex

from nonebot.typing import T_State
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import Event

# 今天是几号星期
WEEK = ['一', '二', '三', '四', '五', '六', '日']
def get_weekday(date: str):
    if date[:2] == '今天':
        index = datetime.date.today().weekday()
    elif date[:2] == '明天':
        index = datetime.date.today().weekday()+1
    else:
        pattern = re.compile(r'\d+')
        res = re.findall(pattern, date)
        assert len(res) <= 3
        res = list(reversed(res))
        res.extend([None]*(3-len(res)))
        day, month, year = res
        if not year:
            year = datetime.date.today().year
        if not month:
            month = datetime.date.today().month
        index = datetime.date(int(year),int(month),int(day)).weekday()
    return WEEK[index]



week_day = on_regex('(.*)是?(星期|周)几', block=False)
@week_day.handle()
async def week_day_handle(bot: Bot, event: Event, state: T_State):
    date, name_ = state['_matched_groups']
    try:
        msg = f"是{name_}{get_weekday(date)}{random.choice(['哦', '喔', ''])}~"
        await bot.send(event, message = msg)
    except ValueError:
        await bot.send(event, message = random.choice(['是你妈的祭日，傻狗', '?', f'{date}你玛呢']))


day = on_regex('(今天)是?几号', block=False)
@day.handle()
async def day_handle(bot: Bot, event: Event, state: T_State):
    date = datetime.date.today().__format__("%m.%d")
    msg = f"今天是{date}{random.choice(['哦', '喔', ''])}~"
    await bot.send(event, message = msg)