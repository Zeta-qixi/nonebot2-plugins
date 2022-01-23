from .db import *
import os
from  time import strftime, localtime
from datetime import datetime, timedelta
import pandas as pd
import re
from .Clock import Clock
from nonebot import on_command, on_message, get_bot, get_driver
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.event import Event, GroupMessageEvent,MessageEvent
from nonebot.adapters.onebot.v11.message import Message
from nonebot.typing import T_State
from nonebot.params import State
from nonebot import require, logger

scheduler = require('nonebot_plugin_apscheduler').scheduler


try:
    master = get_driver().config.master
except:
    master = []



def create_clock_scheduler(clock: Clock):
    '''
    创建闹钟任务
    '''
    logger.info(f"add clock id:{clock.id}")
    async def add_clock():

        await get_bot().send_msg(message_type=clock.type, user_id=clock.user_id, group_id=clock.user_id, message=clock.content)          
        if clock.ones == 1:
            del_clock_db(clock.id)
            scheduler.remove_job(f"clock_{clock.id}")
            logger.info(f"remove clock id:{clock.id}")

    scheduler.add_job(add_clock, "cron", hour=clock.hour, minute=clock.minute, id=f"clock_{clock.id}")

for i in select_all():
    create_clock_scheduler(Clock(i))


def add_clock(uid, content, time, ones, type):
    """添加闹钟"""

    add_clock_db(uid, content, time, ones, type)
    create_clock_scheduler(Clock((new_id() ,type, uid, content, time, ones)))

def del_clock(id):
    """删除闹钟"""

    del_clock_db(id)
    scheduler.remove_job(f"clock_{id}")

def create_time(t):
    """之后加入日 月 星期等条件"""
    return (f"null null null null null {t}")



# 创建闹钟
add = on_command('添加闹钟', aliases={'设置闹钟', '添加提醒事项', 'addclock'})
@add.handle()
async def add_handle(bot: Bot, event: Event, state: T_State = State()):
    uid = event.user_id
    type = event.get_event_name()
    messages = str(event.get_message()).split(' ')
    ones = 1
    content = ''
    try:
        time_ = messages[0]
        content = messages[1]
        if messages[2]:
            ones = 0
    except:
        pass

    content = content if content else '⏰'
    '''
    对time_做验证
    '''
    r = re.match(r'(\d+)[:|\-|：|.](\d+)',time_)

    if time_.startswith('+'):
        h = re.search(r"(\d+)[Hh时]",time_)
        m = re.search(r"(\d+)[Mm分]",time_)
        h=int(h.groups()[0]) if h else 0
        m=int(m.groups()[0]) if m else 0
        time_ = (datetime.now() + timedelta(hours=h, minutes=m)).strftime("%H:%M")
    elif r:
        h, m = r.groups()
        if int(h)>= 24 or int(m) >= 60:
            await bot.send(event, message="时间格式错误～")
            return
        h = f'0{h}' if len(h)==1 else h
        m = f'0{m}' if len(m)==1 else m
        time_ = f'{h}:{m}'
    else:
        await bot.send(event, message="时间格式错误～")
        return

    if 'private' in type:
        add_clock(uid, content, create_time(time_), ones, 'private')
        await bot.send(event, message="添加成功～")
    
    elif 'group' in type:
        gid = event.group_id
        info = await bot.get_group_member_info(group_id=gid, user_id=uid)
        if info['role'] == "member" and uid not in master:
            await bot.send(event, message="你没有该权限哦～")
        else:
            add_clock(gid, content, create_time(time_), ones, 'group')
            await bot.send(event, message="添加成功～")


# # 查看闹钟
# check = on_command('查看闹钟',  aliases={'提醒事项', '闹钟','⏰'})
# @check.handle()
# async def add_handle(bot: Bot, event: Event):
#     try:
#         id = event.group_id
#     except:
#         id = event.user_id
    
#     clock_msg = ''
#     ones=['days', 'ones']
#     for clock in clock_list:
#         if clock.user_id == id:

#             if clock_msg:
#                 clock_msg = clock_msg + f'\n\n{clock.get_info()}'
#             else:
#                 clock_msg = clock_msg + f'{clock.get_info()}'
#     if clock_msg:
#         await bot.send(event, message= Message(clock_msg))
#     else:
#         await bot.send(event, message='目前没有闹钟')
    


# # 删除闹钟
# del_ = on_command('删除闹钟')
# @del_.handle()
# async def del_handle(bot: Bot, event: Event):
#     id = str(event.get_message())
#     if id.isdigit():
#         if del_clock(int(id)):
#             await bot.send(event, message='删除成功')
#             return
#     await bot.send(event, message='失败了')




