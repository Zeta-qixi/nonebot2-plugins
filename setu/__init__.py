
from nonebot import on_command, get_driver
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import Event
from nonebot.adapters.cqhttp.message import Message, MessageSegment

from nonebot.typing import T_State
import os
import sys
import requests
import random
from nonebot.log import logger
import asyncio
import time
from PIL import Image
from io import BytesIO
sys.path.append(os.path.join(os.path.dirname(__file__)))
import Getpic
from aiopic import get_pic
setubot = Getpic.setubot()


try:
    master = get_driver().config.master
except:
    master = []
##变量##
path =os.path.abspath(__file__).split('__')[0]

MAX = 2  # 冲的次数
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
    
    # 尝试3次请求
    for i in range(3):
        try:
            setu_url = setubot.setu_info(int(num), keyword)
            #print(setu_url)
            if setu_url:
                break
        except BaseException as e:
            logger.error(repr(e))

    #获取图片信息url
    if setu_url:
        try:
            pic_list = await get_pic(setu_url)
            for i ,base64 in enumerate(pic_list):
                msg = await bot.send(event, message = MessageSegment.image(f'base64://{base64}'))
                setubot.pic_id.append(msg['message_id'])
                time.sleep(1)
            times[user_id] += num
        except BaseException as e:
            logger.error(repr(e))
            await bot.send(event, message = f'你🐛的太快啦')



recall_setu = on_command('撤回')
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
    
# @on_command('r18', only_to_me=False)
# async def r18(session: CommandSession):
#     user_id=session.ctx['user_id']
#     if(user_id == master[0]):
#         if setubot.R18 ==0:
#             setubot.R18 =1
#         else :
#             setubot.R18 =0
#         await session.send(message = f'r18:{r18type[setubot.R18]}')
#     else:
#         await session.send(message = f'？？')

##-----------------------------------------------_##

# @on_command('stype', only_to_me=False)
# async def mode(session: CommandSession):
#     await session.send(message = f'''Mode: {setubot.mode[setubot.mode_]}
# R18:{r18type[setubot.R18]}
# MAXTIME:{MAX}''')

# @on_command('setutime', only_to_me=False)
# async def showtimes(session: CommandSession):
#     s = ''
#     sum = 0
#     for i,j in times.items():
#         s = s + f'{i} : {j}\n'
#         sum += j
#     await session.send(message = f'{s}sum : {sum}' )
    
# @on_command('cmode', only_to_me=False)
# async def tcmode(session: CommandSession):
#     seq = ''
#     for i,j in enumerate(setubot.mode):
#         seq = seq + f'{i}: {j}\n'
#     seq = seq + f'当前mode: {setubot.mode[setubot.mode_]}\n----------\n选择rank mode～'
#     num=session.current_arg.strip()
#     if not num:
#         num = session.get('message', prompt=seq)
#     await session.send(message = f'mode change: {setubot.Cmode(int(num))}')

