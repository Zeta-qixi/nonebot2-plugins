
from nonebot import on_command
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.params import State, CommandArg

from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from .dynamic import *
from .live import *

push_dynamic = on_command("更新推送", block=True)
'''
直接修改数据库的对应字段
mid filter(动态|直播|过滤) value([0,1],[0,1],['过滤字段'])
'''
@push_dynamic.handle()
async def push_dynamic_handle(bot: Bot, evnet: GroupMessageEvent, msg = CommandArg()):
    uid = event.user_id
    gid = event.group_id

    member_info = await bot.get_group_member_info(group_id=gid, user_id=uid)
    if member_info['role'] == "owner" or member_info['role'] == "admin" or uid in master:
        await bot.send(event, message="你没有该权限哦～")
        return

    try:
        content = str(msg).split(' ')
        mid = int(content[0])

        if content[1] == "动态":
            filter = "dynamic"
        if content[1] == "过滤":
            filter = "dy_filter"
        if content[1] == "直播":
            filter = "live"
        value = content[2]
        if value.isdigit():
            value = int(value)

        update(gid, mid, filter, value)
        await bot.send(event, message=f"ok")
    except:
        await bot.send(event, message=f"失败了～ 发送 mid 字段 内容")
