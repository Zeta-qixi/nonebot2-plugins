from . import tool

from nonebot import on_command, get_driver
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import Event
from nonebot.adapters.cqhttp.message import Message
from nonebot.typing import T_State
import re
try:
    master = get_driver().config.master
except:
    master = []


search = on_command('搜图')
@search.handle()
async def search_handle(bot: Bot, event: Event, state: T_State):
   
    if msg:=event.get_message():
        state['ret'] = msg

@search.got('ret', prompt='图呢')
async def search_got(bot: Bot, event: Event, state: T_State):

    if state['ret']:
        if type(state['ret']) == str:
            state['ret'] = Message(state['ret'])
            
        for msg in state['ret']:
            if msg.type == 'image':
                pic_url = msg.data['url']
                data = await tool.get_image_data(pic_url)
                await search.finish(data)
            else:
                await search.finish('不搜啦、')