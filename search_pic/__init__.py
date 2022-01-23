from . import tool

from nonebot import on_command, get_driver
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.event import Event
from nonebot.adapters.onebot.v11.message import Message
from nonebot.typing import T_State
from nonebot.params import State, CommandArg
import re
try:
    master = get_driver().config.master
except:
    master = []


search = on_command('搜图')
@search.handle()
async def search_handle(bot: Bot, event: Event, state: T_State = State(), msg: Message = CommandArg()):
   
    if msg:
        print(123)
        state['ret'] = msg

@search.got('ret', prompt='图呢')
async def search_got(bot: Bot, event: Event, state: T_State = State()):

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