
from .data import DATA
from nonebot.log import logger
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot import get_driver, on_command, on_message
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from nonebot.adapters.onebot.v11.message import Message, MessageSegment
from nonebot.params import CommandArg
from nonebot.typing import T_State

import re

def union(gid, uid):
    return str((gid << 32) | uid)
    


regular_chat = on_message(priority=99, block=False)
@regular_chat.handle()
async def chat_handle(bot: Bot, event: GroupMessageEvent):
    message = str(event.get_message())
    for id in [(event.user_id, 2), (event.group_id,1), (0,0)]:
        uid = union(*id)
        for pattern in DATA.get_pattern(uid):
            if (res := re.match(pattern=pattern, string=message)):
                ans = DATA.choice(uid, pattern)
                msg = Message(ans.format(*([0]+list(res.groups()))))
                await regular_chat.finish(message=msg)

'''
设置问答

'''

set_respond = on_command('set', block=False)

@set_respond.handle()
async def set_handle(bot: Bot, event: GroupMessageEvent, state: T_State, msg: Message = CommandArg()):

    state['uid'] = event.user_id  
    comman = str(msg).split(' ',1)

    if comman[0]:
        state["key"] = Message(comman[0])
        if len(comman) >1:
            state["value"] = Message(comman[1])


@set_respond.got('key', prompt="设置什么～")
async def set_got(bot: Bot, event: GroupMessageEvent, state: T_State):
    state["key"] = take_message(state["key"])


@set_respond.got('value', prompt="要答什么呢～")
async def set_got2(bot: Bot, event: GroupMessageEvent, state: T_State):

    mseeage = ''
    for msg in (state["value"]):
        if url:=msg.data.get("url"):
            mseeage += str(MessageSegment(msg.type, {"file":url}))
        else:
            mseeage += str(msg)

    DATA.save(state["key"], mseeage , union(state['uid'] , 2))
    await set_respond.finish(message='ok~')


def take_message(message: Message):

    # 提取 Message 信息并对部分符合转义
    keys = ""
    for msg in message:
        if msg.type == 'image':
            keys += f"\[CQ:image,file={msg.data['file']}.*,subType=1]"
        if msg.type == 'text':
            keys += msg.data['text']
        if msg.type == 'at':
            keys += f"\[CQ:at,qq={msg.data['qq']}]"
    return keys + '$' # 完全匹配