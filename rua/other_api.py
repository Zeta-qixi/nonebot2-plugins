'''
三三酱的api平台
http://ovooa.com
'''
import re
from nonebot import on_command, get_driver
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import MessageEvent
from nonebot.adapters.cqhttp.message import Message, MessageSegment
from nonebot.typing import T_State


try:
    master = get_driver().config.master
except:
    master = []
print(master)
api_list ={
    '爬': 'pa',
    '撕了': 'si',
    '吃了': 'chi',
}

pa = on_command('爬', aliases={'撕了', '吃了'})
@pa.handle()
async def pa_handle(bot:Bot, event: MessageEvent):
    print(event.__dict__)
    try:
        msg = str(event.message)
        comm = msg.split('[')[0]
        qq = int(re.search(r"[\[CQ:at,qq=]([0-9].{0,20})[\]]", msg).group(1))
        if qq in master:
            qq = event.sender_id
        await bot.send(event, message = Message(f"[CQ:image,file=http://ovooa.com/API/{api_list[comm]}/api.php?QQ={qq}]"))
    except:
        pass
