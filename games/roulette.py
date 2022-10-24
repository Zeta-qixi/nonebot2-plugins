import os
import re

from nonebot import on_command
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from nonebot.adapters.onebot.v11.message import Message, MessageSegment
from nonebot.params import  CommandArg

from .tools import RouletteGame

PATH =os.path.dirname(__file__)+'/asset/longtu.png'


roulette_group_list = {}

def get_roulette_game(gid):
    roulette_group_list.setdefault(gid, RouletteGame())
    return roulette_group_list[gid]

game = on_command('俄罗斯转盘', block=True)
fill = on_command('装填', aliases={'填装'}, block=True)
duel = on_command('决斗', aliases={'⚔️'}, block=True)
shooting = on_command('开枪', block=True)
gameover = on_command('结束', block=True)


@game.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    await game.finish(message=RouletteGame().rule)



@fill.handle()
async def _(bot: Bot, event: GroupMessageEvent, nums: Message = CommandArg()):
    roulette_game    =      get_roulette_game(event.group_id)
    _, bullet, _     =      roulette_game.get_status()

    if bullet > 0:
        await fill.finish(message='已有装填, 请【开枪】')

    nums = int(str(nums))
    if nums >= 6 or nums<=0:
        msg  =   MessageSegment.image(f'file://{PATH}')
        await fill.finish(message=msg)
    else:
        roulette_game.set_bullet(nums)
        await fill.finish(message=f'装填成功, [子弹数 {nums}/6]')



@duel.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    message = str(event.message)

    if uid := re.search('\[CQ:at,qq=(\d+)\]', message):
        qq1              = event.user_id
        qq2              = int(uid.groups()[0])
        
        if qq1 == qq2:
            msg  =   MessageSegment.image(f'file://{PATH}')
            duel.finish(message=msg)
        roulette_game    = get_roulette_game(event.group_id)
        _, _, duel_time  = roulette_game.get_status()

        if duel_time:
            await duel.finish(message='现在正在进行对决⚔️')
            return
        
        roulette_game.set_bullet(1)
        roulette_game.set_duel(qq1, qq2)
        await duel.finish(message=f'装填子弹1, 开始对决吧！')

    else:
        await duel.finish(message='请指定对象⚔️')



@shooting.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    roulette_game              =    get_roulette_game(event.group_id)
    times, bullet, duel_time   =    roulette_game.get_status()

    if bullet == 0:
        await shooting.finish(message=f'现在没有子弹~')
 
    
    user_id    =    event.user_id
    if duel_time:
        if user_id not in roulette_game.get_member():
            await shooting.finish(message='现在正在进行对决⚔️')


        res = roulette_game.shoot()
        if res == 0:
            members = roulette_game.get_member()
            other = members[0] if members[1] == user_id else members[1]
            await shooting.send(message=Message(f'砰！还有{times-1}轮, 轮到你了[CQ:at,qq={other}]'))
            if times - 1 == 1:
                await shooting.finish(message=Message(f'直接给你[CQ:face,id=169], 砰！你死了'))
        else:
            roulette_game.set_bullet(0)
            await shooting.finish(message=f'砰！ 你死了, 游戏结束')

    else:
        res = roulette_game.shoot()
        if res == 0:
            roulette_game.member.append(event.user_id)
            await shooting.finish(message=f'砰！ 还有{times-1}轮, 剩余子弹{bullet}')
        else:
            roulette_game.set_bullet(0)
            await shooting.finish(message=f'砰！ 你死了, 游戏结束')
    


@gameover.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    roulette_game       =   get_roulette_game(event.group_id)
    times, bullet,_     =   roulette_game.get_status()

    if times == bullet and bullet > 0:
        uid = roulette_game.random_shoot()
        roulette_game.set_bullet(0)
        await gameover.finish(message=Message(f'[CQ:at,qq={uid}] [CQ:face,id=169]砰！ 你死了'))
