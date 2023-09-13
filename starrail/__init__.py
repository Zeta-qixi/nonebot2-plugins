
import os
import asyncio
from nonebot.params import CommandArg
from nonebot import on_regex, on_command
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.event import Event, GroupMessageEvent
from nonebot.adapters.onebot.v11.message import Message, MessageSegment
from nonebot.log import logger
from nonebot.typing import T_State

from .role import get_role

collection_id = [
    {'name': '初始镜像', 'ids':[1996095]},
    {'name': '小橙子阿', 'ids':[1998643]},
    {'name': '星穹中心', 'ids':[2029394, 2009142, 2038092]},
]
index = 0

gl = on_command("更换攻略")
@gl.handle()
async def _(bot: Bot, event: Event, state: T_State, ids: Message = CommandArg()):
    if ids:
        state['ids'] = ids
        

@gl.got('ids', prompt="\n".join([f"{i}:{d['name']}" for i, d in enumerate(collection_id)]))
async def _(bot: Bot, event: Event, state: T_State):
    global index
    index = int(str(state['ids']))
    await gl.finish('ok')


cx = on_regex("^#(.*)攻略$")
@cx.handle()
async def _(bot: Bot, event: Event, state: T_State):
    name = state['_matched_groups']
    

    tasks = [asyncio.create_task(get_role(name[0], collection_id[index]['ids'])) for index in range(3)]
    picb64_list = await asyncio.gather(*tasks)
        

    if picb64_list:
        await cx.finish(message=[MessageSegment.image(byte) for byte in picb64_list])
    else:
        await cx.finish(message="找不到角色哦~")