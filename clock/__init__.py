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
from nonebot.params import CommandArg
from nonebot.typing import T_State
from nonebot import require, logger

scheduler = require('nonebot_plugin_apscheduler').scheduler


try:
    master = get_driver().config.master
except:
    master = []

CLOCK_DATA = {}


def create_clock_scheduler(clock):
    '''
    创建闹钟任务
    '''
    CLOCK_DATA[clock.id] = clock

    async def add_clock():
        if clock.verify_today():
            await get_bot().send_msg(message_type=clock.type, user_id=clock.user, group_id=clock.user, message=clock.content)          
            if clock.ones == 1:
                del_clock_db(clock.id)
                scheduler.remove_job(f"clock_{clock.id}")

    scheduler.add_job(add_clock, "cron", hour=clock.hour, minute=clock.minute, id=f"clock_{clock.id}")

for i in select_all():
    
    c = Clock.init_from_db(i)
    
    create_clock_scheduler(c)


def add_clock(**kwargs):
    """添加闹钟"""
    kwargs['id'] = new_id()
    clock = Clock((kwargs))
    add_clock_db(clock)
    create_clock_scheduler(clock)

def del_clock(id: int):
    """删除闹钟"""
    
    del_clock_db(id)
    del(CLOCK_DATA[id])
    scheduler.remove_job(f"clock_{id}")
    return True



def get_time(time_):
    t = None
    r = re.match(r'(\d+)[:|\-|：|.](\d+)',time_)
    if time_.startswith('+'):
        h = re.search(r"(\d+)[Hh时]",time_)
        m = re.search(r"(\d+)[Mm分]",time_)
        h=int(h.groups()[0]) if h else 0
        m=int(m.groups()[0]) if m else 0
        t = (datetime.now() + timedelta(hours=h, minutes=m)).strftime("%H:%M")

    elif r:
        h, m = r.groups()
        if int(h) < 24 or int(m) < 60:
            h = f'0{h}' if len(h)==1 else h
            m = f'0{m}' if len(m)==1 else m
            t = f'{h}:{m}'

    return t
        

# 创建闹钟
add_clock_qq = on_command('添加闹钟', aliases={'设置闹钟', '添加提醒事项', 'addclock'})
@add_clock_qq.handle()
async def _(bot: Bot, event: Event, state: T_State, messages:Message = CommandArg()):
    uid = event.user_id
    type = event.get_event_name()
    messages = str(messages).split(' ')
    ones = 1
    content = '⏰'
    try:
        time_ = messages[0]
        content = messages[1]
        if messages[2]:
            ones = 0
    except:
        pass

    time_ = get_time(time_)
    if not time_:
        await add_clock_qq.finish(message="时间格式错误")


    data = {
        'user' : uid,
        'content' : content,
        'time' : time_,
        'ones' : ones,
        'type' : 'private'
    }
       
    if 'group' in type:
        gid = event.group_id
        info = await bot.get_group_member_info(group_id=gid, user_id=uid)
        if info['role'] == "member" and uid not in master:
            await add_clock_qq.finish(message="你没有该权限哦～")

        data['type'] = 'group'
        data['user'] = gid


    add_clock(**data)
    await add_clock_qq.finish(message="添加成功～")


# # 查看闹钟
check = on_command('查看闹钟',  aliases={'提醒事项', '闹钟','⏰'}, block=True)
@check.handle()
async def add_handle(bot: Bot, event: Event):
    try:
        uid = event.group_id
    except:
        uid = event.user_id
    
    clock_msg = []
    ones=['days', 'ones']
    for id in CLOCK_DATA:
        clock = CLOCK_DATA[id]
        if clock.user == uid:
            clock_msg.append(clock.get_info())
    if clock_msg:
        await bot.send(event, message= Message('\n'.join(clock_msg)))
    else:
        await bot.send(event, message='目前没有闹钟')
    


# 删除闹钟
del_ = on_command('删除闹钟', block=True)
@del_.handle()
async def del_handle(bot: Bot, event: Event, id = CommandArg()):
    id = int(str(id))
    if id in CLOCK_DATA:
        del_clock(id)
        await del_.finish(message='删除成功')
    else:
        await del_.finish(message='没有这个id')
    await del_.finish(message='失败了')





