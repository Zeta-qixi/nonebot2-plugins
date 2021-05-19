import json
import os
import random
import time
import sys

from nonebot import on_command, on_message
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import Event, GroupMessageEvent,MessageEvent, PokeNotifyEvent
from nonebot.adapters.cqhttp.message import Message
from nonebot.rule import to_me
from nonebot.typing import T_State

# -global- #
repeat_stop = False
trigger = {} #重复触发词判定
data = {} #语料数据
ptalk = {} #群回复率
P = 1
focus_id = [] #特别对象 无视概率直接回复
filter_list = []

gpath =os.path.dirname(__file__)
path = gpath +'/data.json'

# 读取数据文件
try:
    with open(path) as f:
        data = json.load(f)
    with open(gpath +'/filter.json') as f:
        filter_list = json.load(f)['f']
except:
    pass

def save_json(keys, values):
    '''
    写数据到json
    '''
    global data
    if keys not in data:
        data.setdefault(keys,[])
        data [keys] = values
    else:  
        for i in values:
            if i not in data[keys]: 
                data[keys].append(i)
                print(str(i))
    
    with open(path, 'w+') as f :
        tojson = json.dumps(data,sort_keys=True, ensure_ascii=False, indent=4,separators=(',',': '))
        f.write(tojson)

chat = on_message(priority=99)
@chat.handle()
async def chat_handle(bot: Bot, event: GroupMessageEvent):
    message = str(event.raw_message)
    group_id = event.group_id
    user_id = event.user_id
    
    global ptalk
    ptalk.setdefault(group_id,P)
    trigger.setdefault(group_id,' ')
   

    for i in data:
        if i in message :
            print(i)
            if len(i) > 3 or i == message:
                # 重复回复的
                if trigger[group_id] != i : 
                    if random.random() < ptalk[group_id] or user_id in focus_id:
                        await bot.send(event,message=Message(random.choice((data[i]))))

                        if repeat_stop:
                            trigger[group_id] = i


setp = on_command('setP', aliases={"setp"}, rule = to_me())
@setp.handle()
async def setp_handle(bot: Bot, event: Event, state: T_State):
    group_id = event.group_id
    user_id = event.user_id
    if user_id in bot.config.master:
        args = str(event.get_message()).strip()
        global ptalk
        if args:
            ptalk[group_id] = float(args)
            await setp.finish(f'现在的回复率为：{ptalk[group_id]}')





set_respond = on_command('set')
@set_respond.handle()
async def setp_handle(bot: Bot, event: Event, state: T_State):

    comman = str(event.get_message()).split()
    if comman:
        print(comman)
        state["key"] = comman[0]
        if len(comman) >1:
            state["value"] = comman[1:]


@set_respond.got('key', prompt="设置什么～")
async def setp_got(bot: Bot, event: Event, state: T_State):
    try:
        
        comman = str(event.get_message()).split()
        state["key"] = comman[0]

        if ",url=" in state["key"] :
            state["key"] = state["key"].split(",url=")[0]

        if len(comman) >1:
            
            state["value"] = comman[1:]
            #录入库
            save_json(state["key"], state["value"])
            await set_respond.finish(message= f'ok~')
    except:
        await set_respond.finish(message= f'失败了QAQ')

def filter(word):
    for i in filter_list:
        if i in word:
            return True
    return False

@set_respond.got('value', prompt="要答什么呢～")
async def setp_got2(bot: Bot, event: Event, state: T_State):
    try:
        
        state["value"] = str(event.get_message()).split()

        if  filter(state["key"]):
            await set_respond.finish(Message("[CQ:image,file=cab2ae806af6b0a7b61fdd8534b50093.image,url=http://gchat.qpic.cn/gchatpic_new/1019289695/648868273-2230236507-CAB2AE806AF6B0A7B61FDD8534B50093/0?term=3]"
  ))
            return
        #录入库
        save_json(state["key"], state["value"])
        await set_respond.finish(message= f'ok~')
    except:
        await set_respond.finish(message= f'失败了QAQ')

