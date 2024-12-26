import os
import json
from nonebot.params import  CommandArg
from nonebot.adapters.onebot.v11.bot import Bot, Message
from nonebot import get_bot
from nonebot import require, on_command
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import GroupMessageEvent
from nonebot.adapters.onebot.v11.event import Event
from .manga_scraping import update
from .manga_subscribers import auto_notify



scheduler = require('nonebot_plugin_apscheduler').scheduler
@scheduler.scheduled_job('cron', hour='*/4', minute="0", id='comic_pusher')
async def push_comic():
    bot = get_bot()
    await update()
    await auto_notify(bot)


manga = on_command('漫画')
@manga.handle()
async def _(event: GroupMessageEvent):
    bot = get_bot()
    await update()
    await auto_notify(bot)

