import requests 
import re
import os
import json
from nonebot import on_command
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import (MessageEvent, PokeNotifyEvent)
from nonebot.adapters.cqhttp.message import Message, MessageSegment
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.typing import T_State
from nonebot.log import logger
import nonebot
from nonebot import require
master = nonebot.get_driver().config.master

try:
    path = os.path.dirname(__file__) + "/data.json"
    with open(path) as f: 
        data = json.load(f)
        API_Key = data['API_Key']
        Secret_Key = data['Secret_Key']
except:
    logger.error('请填写api key')
    API_Key = ''
    Secret_Key = ''

# client_id 为官网获取的AK， client_secret 为官网获取的SK
host = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={API_Key}&client_secret={Secret_Key}'
response = requests.get(host)

access_token = response.json()["access_token"]
request_url = 'https://aip.baidubce.com/rest/2.0/solution/v1/img_censor/v2/user_defined'
request_url = request_url + "?access_token=" + access_token
headers = {'content-type': 'application/x-www-form-urlencoded'}

def porn_pic(pic_url):
    params = {"imgUrl":pic_url}
    response = requests.post(request_url, data=params, headers=headers)
    data = response.json()['data'][0]
    print(data)
    if data['type'] == 1:

        score = round((data['probability']) * 100,2)
        return (score)
    else:
        pass
        # 不是二次元

setu_score = on_command('评分')
@setu_score.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    uid = event.user_id
    gid = event.group_id
    member_info = await bot.get_group_member_info(group_id=gid, user_id=uid)
    if member_info['role'] == "owner" or uid in master:
        if str(event.message) != '':
            state['ret'] = str(event.message)
    else:
        state['ret'] = False
        await bot.send(event, message='你没有权限哦～')
        


@setu_score.got("ret", prompt="色图呢?")
async def setu_got(bot: Bot, event: MessageEvent, state: T_State):


        if state['ret']:

            ret = re.search(r"\[CQ:image,file=(.*)?,url=(.*)\]", str(state['ret']))
            pic_url = ret.group(2)
            s = porn_pic(pic_url)

            await bot.send(event, message=MessageSegment.image(pic_url)+f'色图评分为{s}')


