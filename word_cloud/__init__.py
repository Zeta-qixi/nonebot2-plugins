import base64
import json
import os
from PIL import Image
from collections import defaultdict
from wordcloud import WordCloud
from io import BytesIO
import jieba
import numpy as np

from nonebot import on_command, on_message
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import Event, GroupMessageEvent
from nonebot.adapters.cqhttp.message import MessageSegment
from nonebot.typing import T_State



gpath = os.path.dirname(__file__)
path = gpath +'/data.json'
font = gpath + '/MSYH.TTC'
DATA = defaultdict(dict)

save_ = on_command('保存一下')
generator = on_command('生成词云')
get_chat = on_message(priority=1, block=False)



@save_.handle()
async def chat_handle(bot: Bot, event: GroupMessageEvent):
    with open(path, 'w+') as f :
            tojson = json.dumps(DATA,sort_keys=True, ensure_ascii=False, indent=4,separators=(',',': '))
            f.write(tojson)


@get_chat.handle()
async def chat_handle(bot: Bot, event: GroupMessageEvent):
    message = str(event.raw_message)
    group_id = event.group_id
    if '[CQ:' in message:
        return
    for word in list(jieba.cut(message, cut_all=False)):
        if len(word) > 1:
            DATA[group_id].setdefault(word, 0)
            DATA[group_id][word] += 1

    

@generator.handle()
async def generator_handle(bot: Bot, event: Event, state: T_State):
    group_id = event.group_id

    img = WordCloud(background_color='white', width=550, height=400, font_path=font).fit_words(DATA[group_id])
    img = WordCloud.to_image(img)
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    pic = base64.b64encode(buffer.getvalue()).decode()
    await bot.send(event,message=MessageSegment.image(f'base64://{pic}'))
