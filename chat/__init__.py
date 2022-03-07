import json
import os
import random
import sys
import time
from collections import defaultdict

from nonebot import get_driver, on_command, on_message
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import GroupMessageEvent
from nonebot.adapters.cqhttp.message import Message, MessageSegment
from nonebot.log import logger
from nonebot.typing import T_State


# -global- #
P = 1

try:
    master = get_driver().config.master
except:
    master = []
    logger.info("没有设置master")


gpath =os.path.dirname(__file__)
path = gpath +'/data.json'

def union(gid, uid):
    return str((gid << 32) | uid)
    
# 读取数据文件
try:
    with open(path) as f:
        DATA = json.load(f)
        DATA = defaultdict(dict, DATA)
except:
    DATA = defaultdict(dict)
    logger.info("缺少data.json")

try:
    with open(gpath +'/filter.json') as f:
        FILTER = json.load(f)['f']
except:
    FILTER = []
    logger.info("缺少filter.json")


def save_json(keys:str, values:str, id:str):

    DATA[id].setdefault(keys, [])

    if values not in DATA[id][keys]: 
            DATA[id][keys].append(values)
    with open(path, 'w+') as f :
            tojson = json.dumps(DATA,sort_keys=True, ensure_ascii=False, indent=4,separators=(',',': '))
            f.write(tojson)


chat = on_message(priority=99)
@chat.handle()
async def chat_handle(bot: Bot, event: GroupMessageEvent):
  message = str(event.get_message())
  print(message)


  group_id = event.group_id
  user_id = event.user_id
  
  if random.random() < P:
    for id in [1, group_id]:
        union_id = union(id, 1)
        for keyword in DATA[union_id]:
          if (keyword == message) or (keyword in message and len(keyword) > 3) :
              msg = Message(random.choice((DATA[union_id][keyword])))
              await chat.finish(message=msg)
   

'''
设置问答

'''

def  filter(word):
    for i in FILTER:
        if i in word:
            return True
    return False


set_respond = on_command('set',aliases={"setall"})
@set_respond.handle()
async def set_handle(bot: Bot, event: GroupMessageEvent, state: T_State):
    '''
    setall 回答全覆盖
    '''
    if "setall" in state["_prefix"]["command"]:
        state['gid'] = 1
        state['uid'] = 1
        if event.user_id not in master: 
            await set_respond.finish(Message("[CQ:image,file=cab2ae806af6b0a7b61fdd8534b50093.image]"))
    else:
        state['gid'] = event.group_id
        state['uid'] = event.user_id
    comman = str(event.get_message()).split(' ',1)

    if comman[0] :
        state["key"] = comman[0]
        if len(comman) >1:
            state["value"] = comman[1]

@set_respond.got('key', prompt="设置什么～")
async def set_got(bot: Bot, event: GroupMessageEvent, state: T_State):

    # 提取 cq码中的url
    if ",url=" in state["key"] :
        state["key"] = state["key"].split(",url=")[0]
        

@set_respond.got('value', prompt="要答什么呢～")
async def set_got2(bot: Bot, event: GroupMessageEvent, state: T_State):

    save_json(state["key"], state["value"], union(state['gid'] , 1))
    await set_respond.finish(message='ok~')
    # except BaseException as e:
    #     logger.error(repr(e))
