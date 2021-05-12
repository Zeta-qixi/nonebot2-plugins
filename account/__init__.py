from nonebot import on_command
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import (Event, GroupMessageEvent, MessageEvent)
from nonebot.adapters.cqhttp.message import Message, MessageSegment
from nonebot.typing import T_State

import os
import json

class Data:
    def __init__(self):
        path =os.path.dirname(__file__)
        path = path +'/data.json'
        with open(path) as f:
            self.data = json.load(f)


    def save_json(self):
        with open(path, 'w+') as f :
            tojson = json.dumps(self,data,sort_keys=True, ensure_ascii=False, indent=4,separators=(',',': '))
            f.write(tojson)

    def add_account(self, name, game=None, acc=None, pwd=None):
        self.data[name] = {'name':name, 'game':game, 'acc':acc, 'pwd':pwd}
        self.save_json()

D = Data()

add = on_command('添加账号')
check = on_command('代肝')