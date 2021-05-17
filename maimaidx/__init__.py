
import os

from nonebot import on_command
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import Event
from nonebot.adapters.cqhttp.message import Message, MessageSegment

from nonebot.typing import T_State
from . import maidx

dxbot = maidx.maibot()
random_song = on_command('maimai', aliases={'买买', '麦麦', '舞萌', 'Mai'})


@random_song.handle()
async def maimaidx(bot: Bot, event: Event, state: T_State):


    #获取关键词，数量 并处理
    comman = str(event.get_message()).strip().split(' ')
    keyword = ''
    num = 1

    try:
        if len(comman) ==2:
            num = int(comman[1])
            if num > 4:
                await bot.send(message = f'您搁这抽卡呢？')
                return 0
        Rlist = {'红': 2, '紫': 3, '白':4} #数组的index
        if comman[0][0] in Rlist.keys():
            rank =  Rlist[comman[0][0]]
            lv = comman[0][1:]
            list = dxbot.random_song([lv],num=num, rank=rank)


            
        else:
            lv = comman[0].split('-')

            list = dxbot.random_song(lv,num=num)
    except:
        print('err')
        return

    msg = ''
    for i in list:
        if msg :
            msg += '\n----------------\n'
        msg += i
    await bot.send(event, message = msg)
