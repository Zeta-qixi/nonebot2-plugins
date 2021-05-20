from nonebot import on_command, on_request, on_notice
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import GroupMessageEvent, GroupRequestEvent, Event, GroupBanNoticeEvent
from nonebot.adapters.cqhttp.message import Message, MessageSegment
from nonebot.typing import T_State

change = on_command('更改头衔',aliases={'申请头衔'})
@change.handle()
async def special_title(bot: Bot, event: GroupMessageEvent, state: T_State):
    '''
    群头衔
    '''
    title = str(event.get_message())
    user_id = event.user_id
    group_id = event.group_id
    await bot.set_group_special_title(group_id=group_id, user_id=user_id, special_title=title,self_id=bot.self_id)





