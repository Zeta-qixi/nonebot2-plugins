from nonebot import on_command, get_driver
from nonebot.adapters.cqhttp.event import (Event, MessageEvent)
from nonebot.typing import T_State
from .Action import broadcast
from nonebot.adapters.cqhttp.bot import Bot

bd = on_command('bd')
@bd.handle()
async def handle_first_receive(bot: Bot, event: MessageEvent, state: T_State):
    if (event.user_id) in bot.config.master:
        msg = event.message
        print(msg)
        try: 
            group_id = event.group_id
        except:
            group_id = 0
        await broadcast(bot, msg, group_id)


tet = on_command('雀魂好友房間', aliases={'雀魂好友房间'})
@tet.handle()
async def handled_(bot: Bot, event: MessageEvent, state: T_State):

    state['msg'] = str(event.message)
    state['name'] = str(event.sender.nickname)



@tet.got("bd", prompt = "需要转发吗?")
async def handled_(bot: Bot, event: MessageEvent, state: T_State):
    if state['bd'] in ["要","y","转发", "Y", "好"]:

        msg = f"{state['name']}: 有雀魂吗 {state['msg']}"
        print(msg)
        await broadcast(bot, msg, event.group_id)
    pass