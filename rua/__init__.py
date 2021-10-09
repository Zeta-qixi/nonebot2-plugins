from .rua import *


from nonebot import on_command, get_driver
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import MessageEvent
from nonebot.adapters.cqhttp.message import Message, MessageSegment

from nonebot.typing import T_State


pa = on_command('爬')
@pa.handle()

async def pa_handle(bot:Bot, event: MessageEvent):

    qq = re.search(r"[\[CQ:at,qq=]([0-9].{0,20})[\]]", str(event.message)).group(1)
    assert qq
    await bot.send(event, message = Message(f"[CQ:image,file=http://ovooa.com/API/pa/api.php?QQ={qq}]"))