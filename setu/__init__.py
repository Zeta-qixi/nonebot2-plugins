
from nonebot import on_command, get_driver
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import Event
from nonebot.adapters.cqhttp.message import Message, MessageSegment

from nonebot.typing import T_State
import os
import sys
import requests
import random
sys.path.append(os.path.join(os.path.dirname(__file__)))
from . import Getpic
setubot = Getpic.setubot()

##变量##
path =os.path.abspath(__file__).split('__')[0]




MAX = 2  # 冲的次数
times = {} # 记录冲的次数
r18type= ['关闭','开启']

master = get_driver().config.master

##bot 指令
setu = on_command('setu',aliases={'Setu', 'SETU'})
@setu.handle()
async def setu_handle(bot: Bot, event: Event, state: T_State):

    #获取关键词，数量 并处理
    comman = str(event.message).split(' ')
    keyword = ''
    num = 1
    print(comman)
    # 变量只有一个 判定是keyword还是num
    try:
        if len(comman) == 1: 
            if len(comman[0]) == 1 and comman[0].isdigit():
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
        # setu太多发这图片
        if times[user_id] > MAX:
            times[user_id] = 0
            img_src = path + '/panci.png'
            img = MessageSegment.image(f'file://{img_src}')
            await bot.send(event, message = img)
            return 0
        if int(num) > 3:
            num = 3
            await bot.send(event, message = f'一次最多3张哦～')

    setu_url = setubot.getpic(int(num), keyword)
    if len(setu_url) == 0:
        setu_url = setubot.getpic()  
        await bot.send(event, message = f'找不到{keyword}的色图哦,随机一张吧')
        
    ###获取到url
    for i ,u in enumerate(setu_url):
        img_path = path + f'data/{i}.jpg'
        os.system(f'wget {u} -O {img_path}')
        msg = await bot.send(event, message = MessageSegment.image(f'file://{img_path}'))
        setubot.pic_id.append(msg['message_id'])
        os.system(f'rm {img_path} -f')    
    times[user_id] += num



recall_setu = on_command('撤回')
@recall_setu.handle()
async def recall_setu_handle(bot: Bot, event: Event, state: T_State):

    for id in setubot.pic_id:
        await bot.delete_msg(message_id=id)
    img_src = path + '/recall.png'
    img = MessageSegment.image(f'file://{img_src}')
    await bot.send(event, message = img)
    setubot.pic_id = []

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

