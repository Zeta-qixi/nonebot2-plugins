import asyncio
import random
import time
from datetime import datetime
from os.path import dirname
import requests
import json
from bilibili_api import live
from nonebot import get_bots, on_command, on_message, on_notice, require, get_driver
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import Event
from nonebot.adapters.cqhttp.message import Message, MessageSegment
from nonebot.typing import T_State

master = get_driver().config.master
path = dirname(__file__) +'/data.json'
with open(path) as f:
    liveroom = json.load(f)

class live_:
    def __init__(self):
        #self.liveroom = liveroom_
        self.headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88\
        Safari/537.36 Edg/87.0.664.60',
    'Referer': 'https://www.bilibili.com/'
    }


    def get_info_(self, mid:int):
        url = 'http://api.live.bilibili.com/room/v1/Room/getRoomInfoOld'
        params = {'mid':mid}
        r = requests.get(url ,headers = self.headers, params=params)
        data = r.json()['data']
        return data

    def liveStatus(self, mid:int):
        print('-----')
        url = 'http://api.live.bilibili.com/room/v1/Room/getRoomInfoOld'
        params = {'mid':mid}
        r = requests.get(url,headers = self.headers, params=params)
        status = r.json()['data']['liveStatus']
        return status

    def change_status(self, key:str):
        liveroom[key]['status'] = 0 if liveroom[key]['status'] ==1 else 1
        with open(path, 'w+') as f :
            tojson = json.dumps(liveroom,sort_keys=True, ensure_ascii=False, indent=4,separators=(',',': '))
            f.write(tojson)


live = live_()

scheduler = require('nonebot_plugin_apscheduler').scheduler
@scheduler.scheduled_job('cron', second='*/30', id='live_sched')
async def living():
    for bot in get_bots().values():
    
        for key in liveroom:

            lm = liveroom[key]
            info = live.get_info_(lm['mid'])
            k = info['liveStatus']       
            if k == 1 and lm['status'] == 0:
                
                live.change_status(key)

                title = info['title']
                cover = info['cover']
                url = info['url']
                
                msg = f'你关注的{lm["nickname"]}开播啦！\n#{title}\n{url}[CQ:image,file={cover}]'
                #print(msg)
                await bot.send_group_msg(group_id=648868273, message=msg) 
            elif k == 0 and lm['status'] == 1:
                live.change_status(key)
                msg = f'{lm["nickname"]}下播了。。'
                await bot.send_group_msg(group_id=648868273, message=msg)
            await asyncio.sleep(0.5)


'''
room = live.LiveDanmaku(room_display_id=zeta)
@room.on("LIVE")
def on_live(msg):
    print(msg)
room.connect()

'''
def to_add(id, nickname, name=0):
    if name == 0:
        name = len(liveroom)
        liveroom[id] = {'mid':id, 'nickname': nickname, 'status': 0}

add_up = on_command('添加关注')
@add_up.handle()
async def add(bot: Bot, event: Event, state: T_State):
    user_id = event.user_id
    print(user_id, type(user_id))
    msg = str(event.get_message()).split()
    print(msg)
    if(user_id not in master):
        if msg[0].isdigit:
            id = msg[0]
            nickname = msg[1]
        elif msg[1].isdigit:
            id = msg[1]
            nickname = msg[0]
        else:
            await bot.send(event, message = f'添加失败勒')
            return
        to_add(id, nickname)
        with open(path, 'w+') as f :
            tojson = json.dumps(liveroom,sort_keys=True, ensure_ascii=False, indent=4,separators=(',',': '))
            f.write(tojson)
        await bot.send(event, message = f'添加成功~')
