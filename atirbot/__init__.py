from .special import *
from .request import *
#from .notice import *
from .banatri import *
from .speak import *
from nonebot.typing import T_State
from nonebot import on_command, on_message, get_driver
from nonebot.adapters.cqhttp.event import MessageEvent

try:
    master = get_driver().config.master
except:
    master = []

restart = on_command('restart')
@restart.handle()
async def _restart(bot: Bot, event: MessageEvent, state: T_State):
    uid = event.user_id
    if uid in master:
        await bot.send(event, message = "正在重启...")
        #不兼容
        #await bot.set_restart()
