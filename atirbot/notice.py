from nonebot import on_notice
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import GroupBanNoticeEvent


ban_req = on_notice()
@ban_req.handle()
async def group_ban(bot: Bot, event:GroupBanNoticeEvent):
    '''
    群禁言
    '''
    if (event.sub_type) == "ban":
        pass
    if (event.sub_type) == "lift_ban":
        pass