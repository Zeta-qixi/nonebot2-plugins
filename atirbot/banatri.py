from nonebot import on_notice
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.event import GroupBanNoticeEvent

ban_req = on_notice()
@ban_req.handle()
async def group_ban(bot: Bot, event:GroupBanNoticeEvent):
    '''
    群禁言
    '''
    if (event.sub_type) == "ban":
        if event.user_id == event.self_id:
            await bot.set_group_leave(group_id=event.group_id)
    if (event.sub_type) == "lift_ban":
        pass