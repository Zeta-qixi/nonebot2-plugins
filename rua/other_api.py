'''
三三酱的api平台
http://ovooa.com
'''
import re
from nonebot import on_command, get_driver, on_regex
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import MessageEvent
from nonebot.adapters.cqhttp.message import Message, MessageSegment
from nonebot.typing import T_State

try:
    master = get_driver().config.master
except:
    master = []

api_dict ={
    '爬': 'pa',
    '撕了': 'si',
    '吃了': 'chi',
}
keywords = ''
for k in api_dict:
    if keywords == '':
        keywords = k
    else:
        keywords = keywords + '|' + k
pa = on_regex(f"({keywords})?(.*)", block=False)
@pa.handle()
async def pa_handle(bot:Bot, event: MessageEvent, state: T_State):
    regex = (state['_matched_groups'])
    comm = regex[0]

    if comm:
        qq_ = regex[1].split()[0]
        if qq_.isdigit():
            qq = int(qq_)
        elif 'CQ:at' in qq_:
            qq = re.search(r"\[CQ:at,qq=(.*)\]", qq_).group(1)

        if qq in master:
            qq = event.user_id
        await bot.send(event, message = Message(f"[CQ:image,file=http://ovooa.com/API/{api_dict[comm]}/api.php?QQ={qq}]"))
