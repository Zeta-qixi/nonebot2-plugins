from .browser import get_dynamic_screenshot
from .GetData import *
from ..db import *
import asyncio
import time
from datetime import datetime, timedelta
import random

from nonebot.log import logger

from nonebot import get_bots, on_command, get_driver
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import Event
from nonebot.adapters.cqhttp.message import Message, MessageSegment
from nonebot import require

try:
    master = get_driver().config.master
except:
    master = []

# (id, gid, mid, name, live, is_live, dynamic, lastest_dynamic, dy_filter) 
def get_data_from_db():
    data = []
    for item in (select_dynamic()):
        data.append({
            "gid":item[1], "mid":item[2], "lastest":item[-2], "filter":item[-1]
        })
    return data

scheduler = require('nonebot_plugin_apscheduler').scheduler
@scheduler.scheduled_job('cron', minute='*/10', id='dynamic_sched_')
async def push_dynamic():

    for item in get_data_from_db():
        data = get_dynamic(item['mid'])
        for dy in data['cards'][3::-1]:
            
            dy = Dynamic(dy)
            url = dy.url
            # 判断是否最新的
            if item["lastest"] < dy.time and dy.time > datetime.now().timestamp() - timedelta(minutes=30).seconds:
  
                if dy.type != 1:
                    res_list = await get_dynamic_screenshot(url, item['filter'])

                    for bot in get_bots().values():  
                        msg_pic = MessageSegment.image(f"base64://{res_list['dy']}")
                        await bot.send_group_msg(group_id = item["gid"], message=f'{dy.name}发布了动态: {dy.url}' + msg_pic)
                        if 'pic' in res_list:
                            msg_pic = MessageSegment.image(res_list['pic'])
                            await bot.send_group_msg(group_id = item["gid"], message= msg_pic)

                    # 更新时间
                    update(item["gid"], item["mid"], 'latest_dynamic', dy.time)
         


# 测试用
check_dynamic = on_command("最新动态")
@check_dynamic.handle()
async def check_dynamic_handle(bot: Bot, event):
    for item in get_data_from_db().values():
        data = get_dynamic(item['mid'])
        dy = data['cards'][0]
        dy = Dynamic(dy)
        info = dy.get()   
        url = info[2]
        comman = str(event.get_message())
        if item['gid'] == event.group_id or comman == 'test':
            try:
                res_list = await get_dynamic_screenshot(url, item['filter']) 
                msg_pic = MessageSegment.image(f"base64://{res_list['dy']}")
                await bot.send(event, message=msg_pic)
                if 'pic' in res_list:
                    msg_pic = MessageSegment.image(res_list['pic'])
                    await bot.send(event, message=msg_pic)
            except BaseException as e:

                logger.error(repr(e))




