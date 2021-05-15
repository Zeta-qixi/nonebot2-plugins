

from nonebot import on_command, on_message, on_notice
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import Event, GroupRecallNoticeEvent
from nonebot.adapters.cqhttp.message import Message, MessageSegment
from nonebot.rule import to_me
from nonebot.typing import T_State

rc = on_notice()

@rc.handle()
async def rc_handle(bot: Bot, event: GroupRecallNoticeEvent):
    id = event.message_id
    data = await bot.get_msg(message_id=id)
    raw_msg = data['message']
    sender = data['sender']['nickname']
    msg = f'{sender}撤回了一条信息: {raw_msg}'
    await bot.send_private_msg(user_id=bot.config.master[0], message=Message(msg))
