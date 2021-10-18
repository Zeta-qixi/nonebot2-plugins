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
    
    if event.user_id in master:
        if str(event.message) != '':
            state['ret'] = str(event.message)
    else:
        state["ret"] = False
        await search.finish("不是Master不行的哦~")
    msg = str(event.get_message())




@search.got('ret', prompt='图呢')
async def search_got(bot: Bot, event: Event, state: T_State):

    if state['ret']:
        ret = re.search(r"\[CQ:image,file=(.*)?,url=(.*)\]", str(state['ret']))
        pic_url = ret.group(2)

    data = await tool.get_image_data(pic_url)
    await search.finish(data)