import os
import nonebot
import json
from nonebot import on_command, on_message
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import Event, GroupMessageEvent,MessageEvent, PokeNotifyEvent
from nonebot.adapters.cqhttp.message import  MessageSegment
from nonebot.typing import T_State
from wordcloud import WordCloud
from PIL import Image
from io import BytesIO
import numpy as np
import base64
import jieba
from collections import defaultdict

gpath = os.path.dirname(__file__)
path = gpath +'/data.json'
font = gpath + '/MSYH.TTC'
mask = np.array(Image.open(gpath + '/mask.jpg'))


DATA = defaultdict(dict)

save_ = on_command('保存一下')
@save_.handle()
async def chat_handle(bot: Bot, event: GroupMessageEvent):

    with open(path, 'w+') as f :
            tojson = json.dumps(DATA,sort_keys=True, ensure_ascii=False, indent=4,separators=(',',': '))
            f.write(tojson)

chat = on_message(priority=1, block=False)
@chat.handle()
async def chat_handle(bot: Bot, event: GroupMessageEvent):
    message = str(event.raw_message)
    group_id = event.group_id
    if '[CQ' in message:
        return
    for word in list(jieba.cut(message, cut_all=True)):
        if len(word) > 1:

            DATA[group_id].setdefault(word, 0)
            DATA[group_id][word] += 1

    

generator = on_command('生成词云')
@generator.handle()
async def generator_handle(bot: Bot, event: Event, state: T_State):
    group_id = event.group_id
    text = []
    for word in DATA[group_id]:
        times = DATA[group_id][word]
        text.extend([f'{word} ' for _ in range(times)])
    text = ''.join(text)

    print(DATA[group_id])

    # print('1')
    img = WordCloud(background_color='white', width=600, height=300, font_path=font).generate(text)
    img = WordCloud.to_image(img)
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    pic = base64.b64encode(buffer.getvalue()).decode()
    await bot.send(event,message=MessageSegment.image(f'base64://{pic}'))