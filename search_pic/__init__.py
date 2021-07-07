from . import tool

from nonebot import on_command, get_driver
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import Event
from nonebot.adapters.cqhttp.message import Message, MessageSegment

from nonebot.typing import T_State

try:
    master = get_driver().config.master
except:
    master = []


search = on_command('搜图')
@search.handle()
async def search_handle(bot: Bot, event: Event, state: T_State):
    
    if event.user_id not in bot.config.master:
        search.finish()
    msg = str(event.get_message())
    if 'CQ:image' in msg:
        state["url"] = msg.split('url=')[-1][:-1]



@search.got('url', prompt='图呢')
async def search_got(bot: Bot, event: Event, state: T_State):

    if event.user_id not in master:
        await search.finish("不是Master不行的哦~")
        
    msg = str(event.get_message())

    if 'CQ:image' in msg:
        state["url"] = msg.split('url=')[-1][:-1]

    data = await tool.get_image_data(state["url"])
    await search.finish(data)