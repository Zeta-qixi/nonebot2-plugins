import asyncio
import json
import random
import time
from datetime import datetime
from os.path import dirname
import requests

from nonebot import (get_bots, get_driver, on_command, on_message, on_notice,
                     require)
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import Event
from nonebot.adapters.cqhttp.message import Message, MessageSegment
from nonebot.typing import T_State

try:
    master = get_driver().config.master
except:
    master = []

path = dirname(__file__) +'/data.json'
with open(path) as f:
    liveroom = json.load(f)

class live_:
    def __init__(self):
        self.headers = {
    'user-agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
    'Referer': 'https://www.bilibili.com/'
    }

    def get_info_(self, mid:int):
        url = 'http://api.live.bilibili.com/room/v1/Room/getRoomInfoOld'
        params = {'mid':mid}
        r = requests.get(url ,headers = self.headers, params=params)
        data = r.json()['data']
        return data

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
    
        for room in liveroom:

            lm = liveroom[room]
            info = live.get_info_(lm['mid'])
            k = info['liveStatus']       
            if k == 1 and lm['status'] == 0:
                
                live.change_status(room)

                title = info['title']
                cover = info['cover']
                url = info['url']
                
                msg = f'你关注的{lm["nickname"]}开播啦！\n#{title}\n{url}[CQ:image,file={cover}]'
                #print(msg)
                await bot.send_group_msg(group_id=lm['gid'], message=msg) 
            elif k == 0 and lm['status'] == 1:
                live.change_status(room)
                msg = f'{lm["nickname"]}下播了。。'
                await bot.send_group_msg(group_id=lm['gid'], message=msg)
            await asyncio.sleep(0.5)


'''
room = live.LiveDanmaku(room_display_id=zeta)
@room.on("LIVE")
def on_live(msg):
    print(msg)
room.connect()

'''
def union(gid, uid):
    return (gid << 32) | uid

def to_add(gid: int, bid: int, nickname):
    liveroom[union(gid, bid)] = {'mid':bid, 'nickname': nickname, 'status': 0, 'gid':gid}

add_up = on_command('添加关注')
@add_up.handle()
async def add(bot: Bot, event: Event, state: T_State):
    '''
    >> 添加关注 bid nickname
    '''
    uid = event.user_id
    gid = event.group_id

    member_info = await bot.get_group_member_info(group_id=gid, user_id=uid)
    if member_info['role'] == "member" and uid not in master:
        await bot.send(event, message="你没有该权限哦～")
    else:
        msg = str(event.get_message()).split()
        
        if msg[0].isdigit:
            id = msg[0]
            nickname = msg[1]
        elif msg[1].isdigit:
            id = msg[1]
            nickname = msg[0]
        else:
            await bot.send(event, message = f'添加失败勒')
            return
        to_add(gid, id, nickname)
        with open(path, 'w+') as f :
            tojson = json.dumps(liveroom,sort_keys=True, ensure_ascii=False, indent=4,separators=(',',': '))
            f.write(tojson)
        await bot.send(event, message = f'添加成功~')

check_live = on_command("谁在直播")
@check_live.handle()
async def check(bot: Bot, event: Event, state: T_State):
    msg = ''
    for bid in liveroom:
        lm = liveroom[bid]
        if lm['status'] == 1:
            info = live.get_info_(lm['mid'])
            url = info['url']
            if msg != '':
                msg = msg+'\n'
            msg = msg + f'{lm["nickname"]}在直播\n({info["title"]}){url}'
            if msg != '':
                await bot.send(event, message = (msg))
            else:
                await bot.send(event, message = "没有人在直播")
