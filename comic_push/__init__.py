import os
import json
from .pusher import *
from nonebot import get_bot
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



scheduler = require('nonebot_plugin_apscheduler').scheduler
@scheduler.scheduled_job('cron', hour='*/1', minute="0", id='comic_pusher')
async def push_comic():
    for uid in data:
        for cid in data[uid]:
            total, title, _, url = await aio_crawler(cid)
            if total > int(data[uid][cid]):
                data[uid][cid] = total
                update()

                msg = f"漫画{title}更新了\n:{url}"
                await get_bot().send_msg(message_type='private', user_id=int(uid), message=msg)




