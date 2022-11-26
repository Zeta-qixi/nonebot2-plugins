from .browser import get_dynamic_screenshot
from .GetData import get_dynamic, Dynamic
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

    return [{"gid":item[1], "mid":item[2], "lastest":item[-2],  
             "filter":item[-1]} for item in (select_dynamic())]


scheduler = require('nonebot_plugin_apscheduler').scheduler
@scheduler.scheduled_job('cron', minute='*/10', id='dynamic_sched_', )
async def push_dynamic():
    
    for item in get_data_from_db():
        data = get_dynamic(item['mid'])
        
        msg_pic = ['发布有新的动态～']
        for dy in data['cards'][3::-1]: # 前3条 倒序 
            dy = Dynamic(dy)
            url = dy.url
            if item["lastest"] < dy.time and dy.type != 1: # 判断最新与转发
                try:
                    res_list = await get_dynamic_screenshot(url, item['filter'])
                    msg_pic.append(MessageSegment.image(f"base64://{res_list['dy']}"))
                    for img in res_list.get('img_url', []):
                        msg_pic.append(MessageSegment.image(file=img))
                    update(item["gid"], item["mid"], 'latest_dynamic', dy.time)
                except Exception as e:
                    logger.error(repr(e))
                    
        await send_forward_msg_group(get_bot(), group_id = item["gid"], message=msg_pic) 

         
# 测试用
check_dynamic = on_command("最新动态")
@check_dynamic.handle()
async def check_dynamic_handle(bot: Bot, event):
    
    for item in get_data_from_db():
        data = get_dynamic(item['mid'])
        dy = data['cards'][0]
        dy = Dynamic(dy)
      
        url = dy.url
        
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