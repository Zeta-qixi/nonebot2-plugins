
from nonebot import on_command, get_driver, on_regex
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import Event
from nonebot.adapters.cqhttp.message import Message, MessageSegment
from nonebot.typing import T_State
from nonebot.log import logger
import re
import os
import sys
import requests
import random
import asyncio
import time
from PIL import Image
sys.path.append(os.path.join(os.path.dirname(__file__)))
from Getpic import SetuBot

try:
    master = get_driver().config.master
except:
    master = []

##变量##
path =os.path.dirname(__file__) + '/data'

## setubot
class setubot(SetuBot):
    def __init__(self):
        super(setubot, self).__init__()
        self.pic_message = {}

    def push_pic_id(self, uid, pid):
        self.pic_message.setdefault(uid, [])
        self.pic_message[uid].append(pid)

setubot = setubot()

setu = on_command('setu',aliases={'Setu', 'SETU', '色图'})
@setu.handle()
async def setu_handle(bot: Bot, event: Event, state: T_State):

    uid = event.user_id
    
    comman = str(event.message).rsplit(' ', 1)
    keyword = ''
    num = 1
    # 变量只有一个 判定是keyword还是num
    if comman[-1].isdigit() and len(comman[-1]) == 1:
        num = int(comman[-1])
        if len(comman)>=2:
            keyword = comman[0]
    else:
        keyword = str(event.message)
    num = 3 if num > 3 else num
        
    if ret := re.search(r'(画师|作者|搜[索图]|推荐)\s?(.*)', keyword):
        if ret.group(1) == '推荐':
            res, res_data = await setubot.get_setu_recommend(int(ret.group(2)),num)
        elif ret.group(1) in ['搜索', '搜图']:
            res, res_data = await setubot.get_setu_by_id(int(ret.group(2)))
        else:
            res, res_data = await setubot.get_setu_artist(ret.group(2), num)
    else:
        res, res_data = await setubot.get_setu_base(keyword, num)

    if res == 1000:
        for info, pic_path in (res_data):
            image = MessageSegment.image(f'file://{pic_path}')
            msg = await bot.send(event, message = info + image)
            setubot.push_pic_id(uid, msg['message_id'])

    elif res == 1001:
        msg = '好像不能发送图片了..'
        for url in (res_data):
            msg = f'{msg}\n{url}'
        await bot.send(event, message = msg)
    elif res == 1100:
        await bot.send(event, message = '你🐛的太快啦')
        
recall_setu = on_regex('撤回色图|太[涩色瑟]了', block=False)
@recall_setu.handle()
async def recall_setu_handle(bot: Bot, event: Event, state: T_State):

    id = event.user_id
    for pid in setubot.pic_message[id]:
        await bot.delete_msg(message_id=pid)
        setubot.pic_message[id].remove(pid)
    img_src = path + '/recall.png'
    await bot.send(event, message = MessageSegment.image(f'file://{img_src}'))




chack_pixiv = on_command("查询个人信息")
@chack_pixiv.handle()
async def chack_handle(bot: Bot, event: Event, state: T_State):
    pass