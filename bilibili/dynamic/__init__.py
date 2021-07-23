from .browser import get_dynamic_screenshot
from .GetData import *
from ..db import *
import asyncio
import time
from datetime import datetime, timedelta
import random

from nonebot import get_bots, on_command, get_driver
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import Event
from nonebot.adapters.cqhttp.message import Message, MessageSegment
from nonebot import require

try:
    master = get_driver().config.master
except:
    master = []



def get_data_from_db():
    dict = {}
    for i, item in enumerate(select_dynamic()):
        dict[i] = {
            "gid":item[0], "mid":item[1], "lastest":item[4]
        }
    return dict


scheduler = require('nonebot_plugin_apscheduler').scheduler
@scheduler.scheduled_job('cron', minute='*/30', id='dynamic_sched_')
async def push_dynamic():

    for item in get_data_from_db().values():
        data = get_dynamic(item['mid'])
        for dy in data['cards'][3::-1]:
            
            dy = Dynamic(dy)
            url = dy.url
            # 判断是否最新的
            if item["lastest"] < dy.time and dy.time > datetime.now().timestamp() - timedelta(minutes=30).seconds:
                if dy.type != 1:
                   
                    base64 = await get_dynamic_screenshot(url) 
                    msg_pic = MessageSegment.image(f'base64://{base64}')
                    
                    # 更新时间
                    upadte(item["gid"], item["mid"], 'latest_dynamic', dy.time)
                    for bot in get_bots().values():
                        print(dy.time, item["lastest"])
                        await bot.send_group_msg(group_id = item["gid"], message=f'{dy.name}发布了动态: {dy.url}' + msg_pic)


check_dynamic = on_command("最新动态")
@check_dynamic.handle()
async def check_dynamic_handle(bot: Bot, event):

    for item in get_data_from_db().values():
        data = get_dynamic(item['mid'])
        dy = data['cards'][0]
        dy = Dynamic(dy)
        info = dy.get()   
        url = info[2] 
        if item['gid'] == event.group_id:
            base64 = await get_dynamic_screenshot(url) 
            msg_pic =  MessageSegment.image(f'base64://{base64}')
            await bot.send(event, message=msg_pic)


push_dynamic = on_command("推送动态")
@push_dynamic.handle()
async def push_dynamic_handle(bot: Bot, event):
    uid = event.user_id
    gid = event.group_id

    member_info = await bot.get_group_member_info(group_id=gid, user_id=uid)
    if member_info['role'] == "member" and uid not in master:
        await bot.send(event, message="你没有该权限哦～")
        return

    try:
        mid = int(str(event.get_message()))
        upadte(gid, mid, 'dynamic', 1)
        await bot.send(event, message=f"ok")
    except:
        await bot.send(event, message=f"失败了～")
    
