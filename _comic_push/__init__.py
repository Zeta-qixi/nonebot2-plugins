import os
import json
from .pusher import *
from nonebot import get_bot, on_command
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.event import MessageEvent
from nonebot import require


try:
    path = os.path.dirname(__file__) + "/data.json"
    with open(path) as f: 
        data = json.load(f)  
except:
    data = {}

def update():
    with open(path, 'w+') as f :
        tojson = json.dumps(data,sort_keys=True, ensure_ascii=False, indent=6,separators=(',',': '))
        f.write(tojson)

comic_add = on_command('追漫')
@comic_add.handle()
async def comic_add_handle(bot: Bot, event: MessageEvent):
    uid = str(event.user_id)
    cid = str(event.get_message())
    if uid not in data:
        data[uid] = {}

    if cid.isdigit():
        cid = f'/{cid}bz/'
        
    title, latest, url_ = crawler(cid)
    data[uid][cid] = latest
    update()

    await bot.send(event, message= f'添加漫画「{title}」（{cid}）')

scheduler = require('nonebot_plugin_apscheduler').scheduler
@scheduler.scheduled_job('cron', hour='*/6', id='comic_pusher')
async def push_comic():
    for uid in data:
        for cid in data[uid]:
            title, latest, url_ = crawler(cid)
            if latest != data[uid][cid]:
                data[uid][cid] = latest
                update()

                msg = f"漫画{title}更新了\n{latest}:{url_}"
                await get_bot().send_msg(message_type='private', user_id=int(uid), message=msg)




