from nonebot import on_notice, logger, get_driver
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import GroupBanNoticeEvent, GroupUploadNoticeEvent
import os

master = get_driver().config.master

ban = on_notice()
@ban.handle()
async def group_ban(bot: Bot, event:GroupBanNoticeEvent):
    '''
    群禁言
    '''
    if (event.sub_type) == "ban":
        pass
    if (event.sub_type) == "lift_ban":
        pass


# upload = on_notice()
# async def _(bot: Bot, event:GroupUploadNoticeEvent):
#     name = '_'.join((event.file.name).split(' '))
#     logger.log(name)
#     url = (event.file.url)
#     logger.log(url)
#     if event.user_id in master:
#         os.popen(f"wget -b -O /root/MCBE-Server-Docker/packs/{name} {url}")
#         logger.log(f"下载文件 {name}")
