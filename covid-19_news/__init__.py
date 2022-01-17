import os
from nonebot import on_regex, on_command, get_bot
from nonebot.adapters.cqhttp.bot import Bot
from collections import  defaultdict
from nonebot.adapters.cqhttp.event import  MessageEvent
from nonebot.typing import T_State
from nonebot import require, logger

from .tools import NewsData
NewsBot = NewsData()
FOCUS = defaultdict(list)

scheduler = require('nonebot_plugin_apscheduler').scheduler
@scheduler.scheduled_job('cron', hour='*/1', minute='0', second='0', misfire_grace_time=60) # = UTC+8 1445
async def update():
    if NewsBot.update_data():
        logger.info(f"[疫情数据更新]{NewsBot.time}")
        for gid in FOCUS.keys():
            bot = get_bot()
            for city in FOCUS.get(gid):
                city_ = NewsBot.data.get(city)
                if city_.today['isUpdated']:
                    await bot.send_group_msg(group_id = gid, message= '关注城市疫情信息更新\n' + city_.main_info)



add_focus = on_command("关注疫情", priority=5)
@add_focus.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    city = str(event.get_message())
    gid = event.group_id
    if NewsBot.data.get(city):
        FOCUS[gid].append(city)
        await add_focus.finish(message=f"已添加{city}疫情推送")
    else:
        await add_focus.finish(message=f"添加失败")


city_news = on_regex(r'^(.{0,6})(疫情.{0,4})', block=True, priority=10)
@city_news.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    city_name, kw = state['_matched_groups']
    if city:= NewsBot.data.get(city_name):
        if kw == '疫情政策':
            await city_news.finish(message=city.policy)
        elif kw == '疫情':
            await city_news.finish(message=f"{NewsBot.time}\n{city.main_info}")
    else:
        await city_news.finish(message="查询的城市不存在或存在别名")

