
import os
from nonebot import on_regex
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import  MessageEvent
from nonebot.typing import T_State
from nonebot import require, logger

from .tools import NewsData
NewsBot = NewsData()

scheduler = require('nonebot_plugin_apscheduler').scheduler
@scheduler.scheduled_job('cron', hour='*/3', minute='0', second='0', misfire_grace_time=60) # = UTC+8 1445
async def update():
    NewsBot.update_data()

city_news = on_regex('(.*)(疫情.*)', block=True)
# city_policy = on_regex('(.*)(疫情政策)', block=True)

@city_news.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    city_name, kw = state['_matched_groups']
    if city:= NewsBot.data.get(city_name):
        if kw == '疫情政策':
            await city_news.finish(message=city.policy)
        elif kw == '疫情':
            await city_news.finish(message=f"{NewsBot.time}\n{city.main_info}")
    else:
        await city_news.finish(message="只限查询国内城市或你地理没学好")

