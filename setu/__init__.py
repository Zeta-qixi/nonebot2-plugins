
from nonebot import on_command, get_driver
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import Event
from nonebot.adapters.cqhttp.message import Message, MessageSegment

from nonebot.typing import T_State
from nonebot.log import logger
import os
import sys
import requests
import random
import asyncio
import time
from PIL import Image
from io import BytesIO

sys.path.append(os.path.join(os.path.dirname(__file__)))

from Getpic import SetuBot

class setubot(SetuBot):
    def __init__(self):
        super(setubot, self).__init__()
        self.pic_id = []

setubot = setubot()

try:
    master = get_driver().config.master
except:
    master = []

##变量##
path =os.path.dirname(__file__)
MAX = 3  # 冲的次数
times = {} # 记录冲的次数
r18type= ['关闭','开启']

## setu
setu = on_command('setu',aliases={'Setu', 'SETU', '色图'})
@setu.handle()

async def setu_handle(bot: Bot, event: Event, state: T_State):
    #获取关键词，数量 并处理
    comman = str(event.message).split(' ')
    keyword = ''
    num = 1
    # 变量只有一个 判定是keyword还是num
    try:
        if len(comman) == 1: 
            if comman[0].isdigit():
                num = int(comman[0])
            else:
                keyword = (comman[0])
        else:
            keyword = comman[0]
            num = int(comman[1])
    except :
        pass   
    user_id = event.user_id  
    if user_id not in times.keys():
        times[user_id] = 0
    if(user_id not in master):
        # 用户限定次数
        # if times[user_id] > MAX:
        #     times[user_id] = 0
        #     img_src = path + '/panci.png'
        #     img = MessageSegment.image(f'file://{img_src}')
        #     await bot.send(event, message = img)
        #     return 0
        if int(num) > 3:
            num = 3
            await bot.send(event, message = f'一次最多3张哦～')
    
    res, res_data = await setubot.get_setu_info(int(num), keyword)  

    if res == 1000:
        for pic_path in (res_data):
            image = MessageSegment.image(f'file://{pic_path}')
            msg = await bot.send(event, message = image)
            setubot.pic_id.append(msg['message_id'])
            time.sleep(1)
        #times[user_id] += num
    elif res == 1001:
        msg = '好像不能发送图片了..'
        for url in (res_data):
            msg = f'{msg}\n{url}'
        await bot.send(event, message = msg)
    elif res == 1100:
        await bot.send(event, message = '你🐛的太快啦')
        
recall_setu = on_command('撤回',aliases={'太色了'})
@recall_setu.handle()
async def recall_setu_handle(bot: Bot, event: Event, state: T_State):

    if setubot.pic_id:
        for id in setubot.pic_id:
            await bot.delete_msg(message_id=id)
        img_src = path + '/recall.png'
        img = MessageSegment.image(f'file://{img_src}')
        await bot.send(event, message = img)
        setubot.pic_id = []

r18 = on_command('r18')
@r18.handle()
async def r18_handle(bot: Bot, event: Event):
    user_id = event.user_id

    if(user_id not in master):
        img_src = path + '/recall.png'
        img = MessageSegment.image(f'file://{img_src}')
        await bot.finish(event, message = img)
    
    r18_type = ['关闭', '开启']
    await bot.send(event, message = r18_type[setubot.tR18()])