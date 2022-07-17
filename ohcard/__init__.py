from nonebot import on_command, on_message, logger, require
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from nonebot.adapters.onebot.v11.message import Message, MessageSegment
from nonebot.params import State, CommandArg

from .data_load import DataLoader, PATH
from .utils import  save_pic, is_exists
from .match_tool import match
import datetime
import time


DL = DataLoader()
OM_MAI_MSG_USER = 0
OH_MAI = DL.data['owner']
USER = DL.data['user']

TIME = 0
FIELD = '25'
def time_field():
    global FIELD
    t = time.localtime()
    FIELD = '25' if (t.tm_hour * 60 + t.tm_min) >= 630 else 'breakfast'

    
is_mai = on_message(priority=0, block=False)
ask = on_command("有无麦卡", block=True)
add_ = on_command("登记麦卡",  block=True)


@ask.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    msg = []
    global TIME
    time_field()
    for uid in OH_MAI:
        if OH_MAI[uid][FIELD] == 0:
            msg.append(f'[CQ:at,qq={uid}]')
    if msg:
        global OM_MAI_MSG_USER
        OM_MAI_MSG_USER = event.user_id
        TIME = time.time()
        header = {'25': '【四件套】【麦卡】\n', 'breakfast':'【早餐】【麦卡】\n'}[FIELD]
        await bot.send(event=event, message= header + Message('\n'.join(msg)) + '\n\n' + '\n'.join(USER.get(str(event.user_id), [])))
        
    else:
        await ask.finish(message="现在没可用的麦卡捏、不如你开一张吧")
def update():
    pass
 

@add_.handle()
async def add_handle(bot: Bot, event: GroupMessageEvent, state: T_State, msg: Message = CommandArg()):

    if is_exists(event.user_id):
        
        uid = str(event.user_id)
        OH_MAI[uid] = {"25": 0, "breakfast":0, "date":str(datetime.date.today() + datetime.timedelta(days=30))}
        DL.save()
        await add_.finish(message="登记成功")
        
    if str(msg) != '':
        state['pic'] = msg
            



@add_.got("pic", "发一下收款码捏～")
async def add_got(bot: Bot, event: GroupMessageEvent, state: T_State):
    
        for msg in Message(state['pic']):
            if msg.type == 'image':
                url = msg.data['url']
                
        uid = str(event.user_id)
        await save_pic(url, uid)
        OH_MAI[uid] = {"25": 0, "breakfast":0, "date":str(datetime.date.today() + datetime.timedelta(days=30))}
        DL.save()
        await add_.finish(message="登记成功")



"""
 询问后LIMIT_TIME 识别目录内用户的图片消息

"""
LIMIT_TIME = 60 * 30
@is_mai.handle()
async def _(matcher: Matcher, bot: Bot, event: GroupMessageEvent):

    uid = str(event.user_id)
    if uid not in OH_MAI:
        return
    global TIME
    global FIELD
    qr = MessageSegment.image(file=f"file://{PATH}{uid}.png")
    
    if event.reply:
        
        if event.reply.sender.user_id == int(bot.self_id) and '【麦卡】' in str(event.reply.message):
            matcher.stop_propagation()
            TIME = 0
            OH_MAI[uid][FIELD] = 1
            await is_mai.finish(message=Message(f'[CQ:at,qq={OM_MAI_MSG_USER}]') + '点餐啦' + qr)
    
    for msg in event.get_message():
        if msg.type == 'image' and time.time() - TIME <= LIMIT_TIME:  
            if await match( msg.data['url']) :  
                TIME = 0
                OH_MAI[uid][FIELD] = 1
                await is_mai.finish(message= "请以本人发的二维码为准捏"+qr)
                

scheduler = require('nonebot_plugin_apscheduler').scheduler
@scheduler.scheduled_job('cron', hour='0', minute='0', second='0', misfire_grace_time=60) # = UTC+8 1445
async def update():
    del_list = []
    for id in OH_MAI:
        OH_MAI[id]["25"] = 0 
        OH_MAI[id]["breakfast"] = 0 
        if OH_MAI[id]["date"] == str(datetime.date.today()):
            del_list.append(id)
    
    for id in del_list:
        del(OH_MAI[id])

    DL.save()
