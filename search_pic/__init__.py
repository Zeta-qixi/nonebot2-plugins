from . import tool

from nonebot import on_command
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import Event
from nonebot.adapters.cqhttp.message import Message, MessageSegment

from nonebot.typing import T_State


search = on_command('搜图')
@search.handle()
async def search_handle(bot: Bot, event: Event, state: T_State):
    msg = event.get_message()
    
    print(msg)
    