from .db import *
import os
from  time import strftime, localtime
from datetime import datetime, timedelta
import pandas as pd
import re
from nonebot import on_command, on_message, get_bots, get_driver
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import Event, GroupMessageEvent,MessageEvent
from nonebot.adapters.cqhttp.message import Message
from nonebot.typing import T_State
from nonebot import require

#加载插件时 获取所有闹钟
# (id, type, user_id, content, c_time, ones) 
clock_data = select_all() #元组list
try:
    master = get_driver().config.master
except:
    master = []

def add_clock(uid, note, time, ones, type):
    """添加闹钟"""
    try:
        add_clock_db(uid, note, time, ones, type)
        clock_data.append((new_id(), type, uid, note, time, ones))
        return True
    except:
        return False

def del_clock(id):
    """删除闹钟"""
    del_clock_db(id)
    for i in clock_data:
        if i[0] == id:
            clock_data.remove(i)
            return True

def create_time(t):
    return (f"null null null null null {t}")

# 创建闹钟
add = on_command('添加闹钟', aliases={'设置闹钟', '添加提醒事项', 'addclock'})
@add.handle()
async def add_handle(bot: Bot, event: Event, state: T_State):
    uid = event.user_id
    type = event.get_event_name()
    content = str(event.get_message()).split(' ')
    note = ''
    ones = 1
    try:
        time = content[0]
        note = content[1]
        if content[2]:
            ones = 0
    except:
        pass

    '''
    对time做验证
    '''
    r = re.match(r'(\d+)[:|\-|：|.](\d+)',time)

    if time.startswith('+'):
        h = re.search(r"(\d+)[Hh时]",time)
        m = re.search(r"(\d+)[Mm分]",time)
        h=int(h.groups()[0]) if h else 0
        m=int(m.groups()[0]) if m else 0
        time = (datetime.now() + timedelta(hours=h, minutes=m)).strftime("%H:%M")
    elif r:
        h, m = r.groups()
        if int(h)>= 24 or int(m) >= 60:
            await bot.send(event, message="时间格式错误～")
            return
        h = f'0{h}' if len(h)==1 else h
        m = f'0{m}' if len(m)==1 else m
        time = f'{h}:{m}'
    else:
        await bot.send(event, message="时间格式错误～")
        return

    if 'private' in type:
        add_clock(uid, note, create_time(time), ones, 'private')
        await bot.send(event, message="添加成功～")
    
    elif 'group' in type:
        gid = event.group_id
        info = await bot.get_group_member_info(group_id=gid, user_id=uid)
        if info['role'] == "member" and uid not in master:
            await bot.send(event, message="你没有该权限哦～")
        else:
            add_clock(gid, note, create_time(time), ones, 'group')
            await bot.send(event, message="添加成功～")
            
# 查看闹钟
check = on_command('查看闹钟',  aliases={'提醒事项', '闹钟','⏰'})
@check.handle()
async def add_handle(bot: Bot, event: Event):
    try:
        id = event.group_id
    except:
        id = event.user_id
    
    clock_msg = ''
    ones=['days', 'ones']
    for i in clock_data:
        if i[2] == id:
            if clock_msg:
                clock_msg = clock_msg + f'\n\n[{i[0]}] ⏰{i[4]} ({ones[(i[5])]})\n备注: {i[3]}'
            else:
                clock_msg = clock_msg + f'[{i[0]}] ⏰{i[4]} ({ones[(i[5])]})\n备注: {i[3]}'
    if clock_msg:
        await bot.send(event, message= Message(clock_msg))
    else:
       
        await bot.send(event, message='目前没有闹钟')
    


# 删除闹钟
del_ = on_command('删除闹钟')
@del_.handle()
async def del_handle(bot: Bot, event: Event):
    id = str(event.get_message())
    if id.isdigit():
        if del_clock(int(id)):
            await bot.send(event, message='删除成功')
            return
    await bot.send(event, message='失败了')

# 闹钟本体

scheduler = require('nonebot_plugin_apscheduler').scheduler
@scheduler.scheduled_job('cron', minute='*/1', second='1', id='clock_')

async def clock_():
    for i in clock_data:
        time_list = i[4].split()
        if strftime("%H:%M", localtime()) == time_list[-1]:
            for bot in get_bots().values():
                s = i[3]
                if s == '':
                    s = '⏰'
                await bot.send_msg(message_type=i[1], user_id=i[2], group_id=i[2], message=s)

            # 删除闹钟            
            if i[5] == 1:
                del_clock_db(i[0])
                clock_data.remove(i)

