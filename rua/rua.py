
from io import BytesIO
import os
from PIL import Image
import requests
from nonebot import on_command, on_notice, get_driver
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.event import Event, PokeNotifyEvent                     
from nonebot.adapters.onebot.v11.message import Message, MessageSegment
from nonebot.typing import T_State
from nonebot.params import State, CommandArg

from .data_source import generate_gif


try:
    master = get_driver().config.master
except:
    master = []


data_dir = os.path.dirname(__file__) + '/data/'
img_src = data_dir +  'output.gif'
img = MessageSegment.image(f'file://{img_src}')


rua_me = on_notice(priority=60)
'''
戳一戳事件
'''      
@rua_me.handle()
async def _t3(bot: Bot, event: PokeNotifyEvent):


    creep_id = event.sender_id  if event.target_id in master else event.target_id
    if creep_id == int(bot.self_id):
        return

    url = f'http://q1.qlogo.cn/g?b=qq&nk={creep_id}&s=160'
    resp = requests.get(url)
    resp_cont = resp.content
    avatar = Image.open(BytesIO(resp_cont))
    #<class 'PIL.JpegImagePlugin.JpegImageFile'>
    generate_gif(data_dir, avatar)
    await bot.send(event, message=img)


    
rua = on_command('rua', block=True)
@rua.handle()
async def rua_handle(bot: Bot, event: Event, state: T_State = State(), msg: Message = CommandArg()):

    for msg_seg in msg:
        if msg_seg.type == 'image':
            state['url'] = msg_seg.data['url']
        else :
            state['url'] = f'http://q1.qlogo.cn/g?b=qq&nk={msg_seg.data["text"]}&s=160'
            

@rua.got("url", prompt="要rua点什么～")
async def rua_got(bot: Bot, event: Event, state: T_State = State()):
    msg = str(state['url'])
    print(msg)

    state['url'] = (msg.split('url=')[-1][:-2])
    resp = requests.get(state['url'])
    resp_cont = resp.content
    try:
        avatar = Image.open(BytesIO(resp_cont))
        generate_gif(data_dir, avatar)
        await bot.send(event, message=img)
    except:
        
        await rua.finish('失败了..')