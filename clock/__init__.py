from .database import db
import os
from  time import strftime, localtime
from datetime import datetime, timedelta
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

"""

"""
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
                db.del_clock(clock.id)
                scheduler.remove_job(f"clock_{clock.id}")

    scheduler.add_job(add_clock, "cron", hour=clock.hour, minute=clock.minute, id=f"clock_{clock.id}")

for i in db.select_all():
    
    create_clock_scheduler(Clock.init_from_db(i))


def add_clock(**kwargs):
    """添加闹钟"""
    kwargs['id'] = db.new_id()
    clock = Clock((kwargs))
    db.add_clock(clock)
    create_clock_scheduler(clock)

def del_clock(id: int):
    """删除闹钟"""
    db.del_clock(id)
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

    messages = str(messages).split(' ', 1)
    ones = 1
    content = '⏰'

    if len(messages) < 2:
        await add_clock_qq.finish(message="添加格式为: “添加闹钟 时间 内容”")

    time_ = get_time(messages[0])
    if not time_:
        await add_clock_qq.finish(message="时间格式错误")

    content = messages[1]
    
    state['content'] = content
    state['time'] = time_


@add_clock_qq.got('ones', prompt="⏰不重复, 设置为每日输入[Y/y]\n设置周几 如周一周三输入[13]\n设置某天，如圣诞输入 [12.25]")
async def _(bot: Bot, event: Event, state: T_State):

    state['ones'] = str(state['ones'])
    ones = 0 if state['ones'] in ['Y', 'y'] else 1
    month, day = 0, 0
    week = ''

    if state['ones'].isdigit():
        week = state['ones']
        ones = 0

    if ret:=re.match('([0-9]{0,2}).([0-9]{1,2})', state['ones']):
        month, day = ret.groups()

    data = {
        'user' : event.user_id,
        'content' : state['content'],
        'time' : state['time'],
        'type' : 'private',
        'ones' : ones,
        'week' : week,
        'day' : day,
        'month' : month
    }
       
    if 'group' in event.get_event_name():

        info = await bot.get_group_member_info(group_id = event.group_id, user_id=event.user_id)
        if info['role'] == "member" and event.user_id not in master:
            await add_clock_qq.finish(message="你没有该权限哦～")

        data['type'] = 'group'
        data['user'] = event.group_id


    add_clock(**data)
    ones_ = {1:'不重复', 0:'重复'}
    await add_clock_qq.finish(message=f"[{ones_[ones]}]添加成功～")


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





