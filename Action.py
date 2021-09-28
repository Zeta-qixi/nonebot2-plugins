from nonebot import on_command, get_driver
from nonebot.adapters.cqhttp.bot import Bot

import nonebot
import asyncio

'''
广播test
'''
ban_group = nonebot.get_driver().config

async def broadcast(bot: Bot, msg, this_group = None):
    list = await bot.get_group_list(self_id=bot.self_id)
    for item in list:
        group = item['group_id']
        if group == this_group:
            continue
        await asyncio.sleep(0.2)
        await bot.send_group_msg(group_id=group,message=msg)
