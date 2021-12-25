import random
import os
from nonebot import on_message, on_notice, get_bot
from nonebot.rule import to_me


from nonebot.typing import T_State
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import MessageEvent, PokeNotifyEvent
from nonebot.adapters.cqhttp.message import MessageSegment

PATH =os.path.dirname(__file__)+'/data/resources/voice/'
VOICE = [f'{PATH}{vf}' for vf in os.listdir((PATH))]
def get_voice() -> str :
    return random.choice(VOICE)

test_voice = on_message(rule=to_me(), priority=55)
@test_voice.handle()
async def voice_handle(bot: Bot, event: MessageEvent, state: T_State):
    await bot.send(event,message= MessageSegment.record(f'file://{get_voice()}'))


rua_me_to_say = on_notice(priority=50,block=False)
@rua_me_to_say.handle()
async def rua_me_to_say_handle(bot: Bot, event: PokeNotifyEvent):

    if event.target_id == int(bot.self_id):
        await bot.send(event,message= MessageSegment.record(f'file://{get_voice()}'))


# scheduler = require('nonebot_plugin_apscheduler').scheduler
# @scheduler.scheduled_job('cron', hour='*/12', id='dynamic_sched_')
# async def say_():
#         await get_bot().send_group_msg(group_id = ["gid"], message= MessageSegment.record(f'file://{get_voice()}'))