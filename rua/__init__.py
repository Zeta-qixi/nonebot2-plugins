from .rua import *


from nonebot import on_command, get_driver
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import MessageEvent
from nonebot.adapters.cqhttp.message import Message, MessageSegment

from nonebot.typing import T_State

'''
三三酱的api平台
http://ovooa.com
'''
try:
    master = get_driver().config.master
except:
    master = []
    
pa = on_command('爬')
@pa.handle()
async def pa_handle(bot:Bot, event: MessageEvent):
    try:
        qq = re.search(r"[\[CQ:at,qq=]([0-9].{0,20})[\]]", str(event.message)).group(1)
        if qq in master:
            qq = event.sender_id
        await bot.send(event, message = Message(f"[CQ:image,file=http://ovooa.com/API/pa/api.php?QQ={qq}]"))
    except:
        pass

si = on_command('撕了')
@si.handle()
async def si_handle(bot:Bot, event: MessageEvent):
    try:
        qq = re.search(r"[\[CQ:at,qq=]([0-9].{0,20})[\]]", str(event.message)).group(1)
        if qq in master:
            qq = event.sender_id
        await bot.send(event, message = Message(f"[CQ:image,file=http://ovooa.com/API/si/?QQ={qq}]"))
    except:
        pass

chi = on_command('吃了')
@chi.handle()
async def chi_handle(bot:Bot, event: MessageEvent):
    try:
        qq = re.search(r"[\[CQ:at,qq=]([0-9].{0,20})[\]]", str(event.message)).group(1)
        if qq in master:
            qq = event.sender_id
        await bot.send(event, message = Message(f"[CQ:image,file=http://ovooa.com/API/chi/?QQ={qq}]"))
    except:
        pass