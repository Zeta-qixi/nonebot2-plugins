'''
俄罗斯转盘
左轮 6孔
'''
from nonebot import  on_command, on_regex
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import GroupMessageEvent
from nonebot.adapters.cqhttp.message import MessageSegment, Message
from .tools import RouletteGame
import os
PATH =os.path.dirname(__file__)+'/asset/longtu.png'


roulette_group_list = {}


def get_roulette_game(gid):
    roulette_group_list.setdefault(gid, RouletteGame())
    return roulette_group_list[gid]

game = on_command('俄罗斯转盘')
fill = on_command('装填', aliases={'填装'})
shooting = on_regex('开枪.*', block=False)
gameover = on_command('结束')


@game.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    await game.finish(message=RouletteGame().rule)


@fill.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    roulette_game = get_roulette_game(event.group_id)

    _, bullet = roulette_game.get_status()
    if bullet > 0:
        await fill.finish(message='已有装填, 请【开枪】')

    nums = int(str(event.message))
    if nums >= 6:
        msg = MessageSegment.image(f'file://{PATH}')
        await fill.finish(message=msg)
    else:
        roulette_game.set_bullet(nums)
        await fill.finish(message=f'装填成功, [子弹数 {nums}/6]')




@shooting.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    roulette_game = get_roulette_game(event.group_id)
    times, bullet = roulette_game.get_status()
    if bullet == 0:
        await fill.finish(message=f'现在没有子弹~')
 
    user_id = event.user_id
    res = roulette_game.shoot()
    if res == 0:
        roulette_game.member.append(event.user_id)
        await fill.finish(message=f'砰！ 还有{times-1}轮, 剩余子弹{bullet}')
    else:
        roulette_game.dead(user_id)
        roulette_game.set_bullet(0)
        await fill.finish(message=f'砰！ 你死了, 游戏结束')
    
@gameover.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    roulette_game = get_roulette_game(event.group_id)
    times, bullet = roulette_game.get_status()
    if times == bullet and bullet > 0:
        uid = roulette_game.random_shoot()
        roulette_game.set_bullet(0)
        await gameover.finish(message=Message(f'[CQ:at,qq={uid}] [CQ:face,id=169]砰！ 你死了'))
