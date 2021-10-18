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

api_dict ={
    '爬': 'pa',
    '撕了': 'si',
    '吃了': 'chi',
}

pa = on_command('爬', aliases={'撕了', '吃了'})
@pa.handle()
async def pa_handle(bot:Bot, event: MessageEvent):

        msg = str(event.raw_message)
        ret = re.search(r"(.*)?\[CQ:at,qq=(.*)\]", msg)
        comm = str(ret.group(1))
        qq = int(ret.group(2))
        if qq in master:
            qq = event.user_id
        await bot.send(event, message = Message(f"[CQ:image,file=http://ovooa.com/API/{api_dict[comm]}/api.php?QQ={qq}]"))

