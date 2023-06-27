
from .mcbe_plugins import get_status as be_status
from .mcje_plugins import get_status as je_status

import asyncio
from nonebot import logger
from nonebot import on_command
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.event import GroupMessageEvent


je_server = [
    # java 服务器地址
    # 192.168.114.514:1234
]

be_server = [
    # be 服务器地址
    # 192.168.114.514:1234
]



mcmc = on_command("mcmc", block=True)
@mcmc.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    
    logger.info('MC')
    coroutine = [je_status(server) for server in je_server] + \
    [be_status(server) for server in be_server]
    
    mc_server_list = await asyncio.gather(*coroutine)
    
    await mcmc.finish(message= "\n==================\n".join([mc.info for mc in mc_server_list]))
    

        
    
    