from nonebot import on_command, on_message, logger, require
from nonebot.typing import T_State
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import GroupMessageEvent
from nonebot.adapters.cqhttp.message import Message, MessageSegment
from .data_load import DataLoader, PATH
from .utils import check_pic, save_pic
import datetime

DL = DataLoader()


DATA = DL.data

ask = on_command("有无麦卡")

@ask.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    msg = ''
    for uid in DATA:
        if DATA[uid]['used'] == 0:
            msg += MessageSegment.at(int(uid))
    if msg:
        await ask.finish(message=f"【麦卡】{msg}")
    else:
        await ask.finish(message="现在没可用的麦卡捏、不如你开一张吧")

def update():
    pass


add_ = on_command("登记麦卡")
@add_.handle()
async def add_handle(bot: Bot, event: GroupMessageEvent, state: T_State):
  
    if (msg:=str(event.get_message())) != '':
        state['pic'] = msg
        



@add_.got("pic", "发一下收款码捏～")
async def add_got(bot: Bot, event: GroupMessageEvent, state: T_State):
        for msg in Message(state['pic']):
            if msg.type == 'image':
                url = msg.data['url']
                uid = str(event.user_id)
                save_pic(url, uid)
                DATA[uid] = {"used": 0, "deadline":str(datetime.date.today() + datetime.timedelta(days=30))}
                DL.save()
                await add_.finish(message="登记成功")


is_mai = on_message(priority=0, block=False)
@is_mai.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    uid = str(event.user_id)

    if uid not in DATA:
        return

    for msg in event.get_message():
        if msg.type == 'image':
            url = msg.data['url']
            if check_pic(url):
                qr = MessageSegment.image(file=f"file://{PATH}{uid}.png")
                DATA[uid]['used'] = 1
                await is_mai.finish(message= "请以本人发的二维码为准捏"+qr)
                

scheduler = require('nonebot_plugin_apscheduler').scheduler
@scheduler.scheduled_job('cron', hour='0', minute='0', second='0', misfire_grace_time=60) # = UTC+8 1445
async def update():
    del_list = []
    for id in DATA:
        DATA[id]["used"] = 0 
        if DATA[id]["deadline"] == str(datetime.date.today()):
            del_list.append(id)
    
    for id in del_list:
        del(DATA[id])

    DL.save()