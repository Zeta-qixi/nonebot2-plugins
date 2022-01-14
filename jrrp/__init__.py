
import nonebot
import random
from nonebot import on_command, require
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import GroupMessageEvent
from nonebot.adapters.cqhttp.message import MessageSegment, Message
from nonebot.typing import T_State
import time
from .jrrp import JrrpGame



scheduler = require('nonebot_plugin_apscheduler').scheduler
master = nonebot.get_driver().config.master

Game = JrrpGame()

jrrp = on_command('jrrp')
duel = on_command('duel')
re_live = on_command('复活')

@jrrp.handle()
async def jrrp_(bot: Bot, event: GroupMessageEvent):
        user_id = event.user_id
        if Game.get(user_id, None):
            await bot.send(event, message= '你今天已经测过人品值了')

        else:
            rp = random.randint(0, 100)
            Game.add_player(user_id, rp)
            await bot.send(event, message=MessageSegment.at(user_id) + f'今日的人品值是:{rp}')

@duel.handle()
async def duel_(bot: Bot, event: GroupMessageEvent):
        user_id = event.user_id

        print(123456)
        msg_seg = event.get_message()[0]
        
        if msg_seg.type == 'at':
            target = int(msg_seg.data['qq'])
            for msg in Game.duel(user_id, target):
                await bot.send(event, message=Message(msg))
                time.sleep(2)

        else:
            await duel.finish(message="请通过at指定对象")
        
@re_live.handle()  
async def duel_(bot: Bot, event: GroupMessageEvent):
       user_id = event.user_id
       if p:=Game.get(user_id, None):
           if not p.live:
                rp = p.rp - 5
                if rp>0:
                    Game.add_player(user_id, rp)
                    await bot.send(event, message="你已经复活了，人品值-5")
                else:
                    await bot.send(event, message="你已经不能复活了")
                


@scheduler.scheduled_job('cron', hour='0', minute='0', second='0', misfire_grace_time=60) # = UTC+8 1445
async def clean():
    Game.clear()
