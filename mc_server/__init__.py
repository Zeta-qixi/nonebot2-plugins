import os
from nonebot import on_command, on_message, on_notice, get_bots
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import (Event, GroupMessageEvent,
                                           MessageEvent)
from nonebot.adapters.cqhttp.message import Message, MessageSegment
from nonebot import require
import time
scheduler = require('nonebot_plugin_apscheduler').scheduler
group = 960349339 #mc群


class mc_server():
    def __init__(self):
        self.player = []
        self.cmd = 'docker logs --tail=1 a2'


    def beat(self):
        """
        查看 docker logs 查看玩家在线情况

        [INFO] Player connected: Atezi alter, xuid: 2535425312726409
        [INFO] Player disconnected: Atezi alter, xuid: 2535425312726409
        """
        msg = os.popen(self.cmd)

        info = []
        for i in msg.readlines():
            if 'Player' in i:
                words = i.split(',')[0].split(': ', 1)
                name = words[1]
                activ = words[0]

                if 'dis' in activ:
                    if name in self.player:
                        self.player.remove(name)
                        info.append(('in', name))
                else:
                    if name not in self.player:
                        self.player.append(name)
                        info.append(('out', name))
                    
                #上线
            
        return info

mcs = mc_server()

ylk = {'in': '加入了游戏～', 'out': '退出了游戏..'}
@scheduler.scheduled_job('cron', minute='*/1', id='mc_server1')
async def lmc_server1():
    msg_list = mcs.beat()
    if msg_list:
        for bot in get_bots().values():
            for (activ, name) in msg_list:
                await bot.send_group_msg(group_id=group,message=f'{name} {ylk[activ]}')
                
