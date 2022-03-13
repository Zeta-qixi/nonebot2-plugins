from .data_load import DataLoader
from nonebot import on_regex, on_command, get_bot
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.message import Message
from nonebot.adapters.onebot.v11.event import  MessageEvent
from nonebot.typing import T_State
from nonebot.params import State, CommandArg
from nonebot import require, logger
from .tools import NewsData

DL = DataLoader('data.json')
NewsBot = NewsData()


'''

 指令:
 #add_focus   #city_news

'''
add_focus = on_command("关注疫情", priority=5, block=True)
@add_focus.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State = State(), city: Message=CommandArg()):
    city = city.extract_plain_text()
    gid = str(event.group_id)
    if NewsBot.data.get(city) and city not in FOCUS[gid]:
        FOCUS[gid].append(city)
        DL.save()
        await add_focus.finish(message=f"已添加{city}疫情推送")
    else:
        await add_focus.finish(message=f"添加失败")


city_news = on_regex(r'^(.{0,6})(疫情.{0,4})', block=True, priority=10)

@city_news.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State = State()):
    city_name, kw = state['_matched_groups']

    if city:= NewsBot.data.get(city_name):
        if kw == '疫情政策':
            await city_news.finish(message=city.policy)
        elif kw == '疫情':
            await city_news.finish(message=f"{NewsBot.time}\n{city.main_info}")
    else:
        await city_news.finish(message="查询的城市不存在或存在别名")



'''

 定时更新 & 定时推送

'''

FOCUS = DL.data
PUSH = {}
for gid in FOCUS.keys():
    for c in FOCUS[gid]:
        PUSH[(gid,c)] = True


scheduler = require('nonebot_plugin_apscheduler').scheduler
@scheduler.scheduled_job('cron', hour='*/1', minute='0', second='0', misfire_grace_time=60) # = UTC+8 1445
async def update():

    if NewsBot.update_data():
        logger.info(f"[疫情数据更新]{NewsBot.time}")

        for gid in FOCUS.keys():
            for c in FOCUS.get(gid):
                city = NewsBot.data.get(c)

                # 判定是否为更新后信息
                if city.today['isUpdated']:
                    # 判定是否未推送
                    
                    if PUSH.get((gid, c), True):
                        PUSH[(gid, c)] = False
                        await get_bot().send_group_msg(group_id = int(gid), message= '关注城市疫情变化\n' + city.main_info)
                
                else:
                    PUSH[(gid, c)] = True


