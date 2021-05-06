
import os

from nonebot import on_command
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import Event
from nonebot.adapters.cqhttp.message import Message, MessageSegment

from nonebot.typing import T_State
from . import maimaidxbot

dxbot = maimaidxbot.maimaidxbot()

random_song = on_command('maimai', aliases={'买买', '麦麦', '舞萌'})


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
        Rlist = {'红': 'E', '紫': 'M', '白':'R'}
        if comman[0][0] in Rlist.keys():
            rank =  Rlist[comman[0][0]]
            lv = comman[0][1:]
            print(rank, lv)
            list = dxbot.get_songIndex_by_lv(rank=rank, lv=lv, num=num)
        else:
            lv = comman[0]
            list = dxbot.get_songIndex_by_lv( lv=lv, num=num)


            
    except:
        print('err')
        return

    for info in list:
        #info --> [classes, name, type, R, cover]
        url = 'https://maimai.sega.jp/storage/DX_jacket/'+info[4]+'.jpg'

        #用正则化后直接输出字符
        img = MessageSegment.image(file=url)
        await bot.send(event, message = f'【{info[0]}】\n{info[1]}\n' + img + f'\n [{info[2]}]{info[3]}')
