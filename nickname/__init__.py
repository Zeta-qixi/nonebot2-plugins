
import json
import os
import nonebot
import json
from nonebot import on_command
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import (Event, MessageEvent)
from nonebot.adapters.cqhttp.message import Message
from nonebot.typing import T_State

path = os.path.dirname(__file__) + "/data.json"

class nickname:
    def __init__(self):
        self.read_data()
        

    def read_data(self):
        with open(path) as f:
            
            try:
                self.data = json.load(f)
                self.data ['0'] = '0'
            except :
                print(path)        

    def my_name(self, id):
        
        id = str(id)
        if id in self.data.keys():
            return(self.data[id])
        else:
            return False

    def take_name(self, id, name):
        self.data[id] = name
        with open(path, 'w+') as f :
            tojson = json.dumps(self.data,sort_keys=True, ensure_ascii=False, indent=6,separators=(',',': '))
            f.write(tojson)

nn = nickname()

set_nickname = on_command('nickname')
@set_nickname.handle()
async def nc_handle(bot: Bot, event: MessageEvent, state: T_State):
    user_id=str(event.user_id)
    name = str(event.get_message())

    try:
        nn.take_name(user_id, name)
        await bot.send(event, message= f'已设置名称:{name}')
    except :
        await bot.send(event, message= f'失败了 呜呜')
    
        

