import os
import json
from nonebot.params import  CommandArg
from nonebot.adapters.onebot.v11.bot import Bot, Message
from nonebot import get_bot
from nonebot import require, on_command
from nonebot.typing import T_State

from nonebot.adapters.onebot.v11.event import Event

from .manga_pusher import get_response as manga_get_response
from .copy_pusher import get_response as copy_get_response, copy_add


scheduler = require('nonebot_plugin_apscheduler').scheduler
@scheduler.scheduled_job('cron', hour='*/4', minute="0", id='comic_pusher')
async def push_comic():
    bot = get_bot()
    await copy_get_response(bot)


manga = on_command('/漫画')
@manga.handle()
async def _(bot: Bot):
    await copy_get_response(bot)


add = on_command('添加漫画')
@add.handle()
async def _(bot: Bot, event: Event, state: T_State,  name: Message = CommandArg()):
    
    copy_add(str(event.user_id), str(name))
    await add.finish('ok')