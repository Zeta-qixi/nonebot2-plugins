from .browser import get_dynamic_screenshot
from .GetData import *
from ..db import *

from nonebot.log import logger
from nonebot import get_bot, on_command, get_driver
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.message import Message, MessageSegment
from nonebot import require
try:
    master = get_driver().config.master
except:
    master = []

# (id, gid, mid, name, live, is_live, dynamic, lastest_dynamic, dy_filter) 
def get_data_from_db():
    data = []
    for item in (select_dynamic()):
        data.append({
            "gid":item[1], "mid":item[2], "lastest":item[-2], "filter":item[-1]
        })
    return data

scheduler = require('nonebot_plugin_apscheduler').scheduler
@scheduler.scheduled_job('cron', minute='*/10', id='dynamic_sched_', )
async def push_dynamic():

    message = []
    for item in get_data_from_db():
        data = get_dynamic(item['mid'])
        for dy in data['cards'][3::-1]: # 前3条 倒序
            
            dy = Dynamic(dy)
            url = dy.url
            # 判断是否最新的
            if item["lastest"] < dy.time:
                update(item["gid"], item["mid"], 'latest_dynamic', dy.time)
                if dy.type != 1:
                    
                    try:
                        res_list = await get_dynamic_screenshot(url, item['filter'])
                        msg_pic = MessageSegment.image(f"base64://{res_list['dy']}")
                        message.append(f'发布了新的动态:\n{dy.url}' + msg_pic)
                       
                        for img in res_list.get('img_url', []):
                            msg_pic = MessageSegment.image(file=img)
                            message.append(msg_pic)
                            
                    except Exception as e:
                        logger.error(repr(e))

    if message:                   
        await send_forward_msg_group(get_bot(),group_id = item["gid"], message= message)

         
# 测试用
check_dynamic = on_command("最新动态")
@check_dynamic.handle()
async def check_dynamic_handle(bot: Bot, event):
    
    for item in get_data_from_db():
        data = get_dynamic(item['mid'])
        dy = data['cards'][0]
        dy = Dynamic(dy)
        info = dy.get()   
        url = info[2]
        
        try:
            res_list = await get_dynamic_screenshot(url, item['filter']) 
            msg_pic = MessageSegment.image(f"base64://{res_list['dy']}")
            await bot.send(event, message=msg_pic)

        except BaseException as e:
            logger.info(url)
            logger.error(repr(e))





# 合并消息
async def send_forward_msg_group(
        bot: Bot,
        group_id: int,
        message,
):

    if isinstance(message, str):
        message = [message]

    def to_json(msg):
        return {"type": "node", "data": {"name": "bilibili", "uin": bot.self_id, "content": msg}}
    await bot.call_api(
        "send_group_forward_msg", group_id=group_id, messages=[to_json(msg) for msg in message]
    )