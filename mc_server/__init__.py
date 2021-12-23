from .beat import *

import os
from nonebot.typing import  T_State
from nonebot import on_regex
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import MessageEvent

start_docker = on_regex('^(启动|关闭)(mc|服务器)', priority=-10)
@start_docker.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):

    active, _ = state['_matched_groups']
    active_dict = {'关闭':'stop', '启动':'start'}
    res = os.popen(f'docker {active_dict[active]} mcbe')
    print(list(res))
    await bot.send(event=event, message= f"已经{active}了哦～")