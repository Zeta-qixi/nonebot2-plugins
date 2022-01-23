import asyncio
import json
import random
import time
from datetime import datetime
import requests
from ..db import *
from nonebot import get_bot, get_driver, on_command,require
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.event import Event
from nonebot.typing import T_State
from nonebot.params import State
from nonebot import logger

try:
    master = get_driver().config.master
except:
    master = []

# (id, gid, mid, name, live, is_live, dynamic, lastest_dynamic, dy_filter) 
LIVE = {}

for i, item in enumerate(select_live()):
    LIVE[i] = {
        "gid":item[1], "mid":item[2], "status":item[5]
    }

"""
获取直播状态
"""

headers = {
'user-agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
'Referer': 'https://www.bilibili.com/'
}

def get_info(mid:int):
    try:
        url = 'http://api.bilibili.com/x/space/acc/info'
        params = {'mid':mid}
        r = requests.get(url ,headers = headers, params=params)
        return r.json()['data']
    except:
        logger.error(f"{mid}---{r.json()}")

scheduler = require('nonebot_plugin_apscheduler').scheduler
@scheduler.scheduled_job('cron', minute='*/1', id='live_sched')
async def living():
    
    for item in LIVE.values():
        await asyncio.sleep(3)
        info = get_info(item["mid"])
        liveroom = info['live_room']
        status = liveroom['liveStatus']
        try:      
            if status == 1 and item['status'] == 0:
            
                item['status'] = 1
                update(item["gid"], item["mid"], "is_live", 1)
                msg = f'你关注的{info["name"]}正在直播！\n#{liveroom["title"]}\n{liveroom["url"]}[CQ:image,file={liveroom["cover"]}]'

                await get_bot().send_group_msg(group_id = item["gid"], message=msg) 

            elif status == 0 and item['status'] == 1:
                item['status'] = 0
                update(item["gid"], item["mid"], "is_live", 0)
                msg = f'{info["name"]}下播了。。'
                await get_bot().send_group_msg(group_id = item["gid"], message=msg)
        finally:
            pass




add_up = on_command('添加关注')
@add_up.handle()
async def add(bot: Bot, event: Event, state: T_State = State()):
    '''
    >> 添加关注 mid
    '''
    uid = event.user_id
    gid = event.group_id

    member_info = await bot.get_group_member_info(group_id=gid, user_id=uid)
    if member_info['role'] == "member" and uid not in master:
        await bot.send(event, message="你没有该权限哦～")
        return

    try:
        mid = (str(event.get_message()))
        if 'uid' in mid:
            mid = mid.split(':')[-1]
        mid = int(mid)
        info = get_info(mid)
        name = info['name']
        if not select_by_field(gid, mid):
            add_focus(gid, mid, name, 1, 0)
            await bot.send(event, message=f"添加关注 {name}")
        else:
            await bot.send(event, message=f"已经在关注 {name} 了哦")
    except KeyError:
        await bot.send(event, message=f"找不到这个id哦～")
    except ValueError:
        await bot.send(event, message=f"请输入正确的id")




del_up = on_command('取消关注', aliases={'不再关注'})
@del_up.handle()
async def add(bot: Bot, event):
    uid = event.user_id
    gid = event.group_id

    member_info = await bot.get_group_member_info(group_id=gid, user_id=uid)
    if member_info['role'] == "member" and uid not in master:
        await bot.send(event, message="你没有该权限哦～")
        return

    try:
        key = str(event.get_message())
        if key.isdigit():
            res = select_by_field(gid, key)
        else:
            res = select_by_field(gid, key, 'name')
            print(res)
        
        mid = res[2]

        delete_by_field(gid, mid)
        await bot.send(event, message=f"已取消关注 {res[3]}")

    except sqlite3.IntegrityError:
        await bot.send(event, message=f"不存在该id")
    except :
        await bot.send(event, message=f"请输入正确的id")
