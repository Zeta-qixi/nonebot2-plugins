from nonebot.adapters.onebot.v11.bot import Bot
from nonebot import on_command, on_message, get_driver
from nonebot.adapters.onebot.v11.message import MessageSegment
from nonebot.adapters.onebot.v11.event import GroupMessageEvent, Message
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.params import CommandArg
from .permission import CHAT_PERM

from .mode_lsit import mode_list

import aiohttp
import time
import json
openai_key = get_driver().config.openai_key
url = 'https://api.openai.com/v1/completions'
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + openai_key,
}

message = {}
last_time = {}

#アトリは、高性能ですから! 
index = 0



AI_PRESET = ""

async def get_chat():
    mode = mode_list[index]
    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, headers=headers, data=json.dumps(mode.mode)) as resp:
            res = await resp.json()
            return res

chat = on_message(rule=CHAT_PERM, priority=90, block=True)
@chat.handle()
async def _(bot: Bot, event: GroupMessageEvent):

    mode = mode_list[index]
    msg = str(event.get_message())
    print(msg)
    if time.time() - last_time.get(event.user_id, 0) > 300:
        message[event.user_id] =  mode.prset + f'{mode.user}{msg}\n{mode.name}' + AI_PRESET
    else:
        message[event.user_id] +=  f'{mode.user}{msg}\n{mode.name}'
    
    mode.mode['prompt'] = message[event.user_id]
    mode.mode['user'] = f"user{event.user_id}"
    res = await get_chat()

    message[event.user_id] += (res['choices'][0]['text']+'\n')
    await chat.send(message = MessageSegment.at(event.user_id) + res['choices'][0]['text'].strip())
    last_time[event.user_id] = time.time()


reset_chat = on_command('重置对话',aliases={'清空对话'},block=True)
@reset_chat.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    last_time[event.user_id] = 0
    await reset_chat.finish(message='重置成功')



set_preset = on_command('/chat前置',block=True)
@set_preset.handle()
async def _(bot: Bot, event: GroupMessageEvent, messages:Message = CommandArg()):
    global AI_PRESET
    AI_PRESET = str(messages)
    await reset_chat.finish(message='设置成功')



get_params = on_command('/chat', block=True)
@get_params.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State, msg: Message = CommandArg()):

    if msg:
        state['ret'] = msg
    else:
        using = {index :'●'}
        await get_params.send(message = '\n'.join([f'{using.get(i, "○")}{i}.{c.mode_name}' for i, c in enumerate(mode_list)]))



@get_params.got('ret', prompt='选择更改的mode')
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
        global index
        assert index < len(mode_list)
        index = int(str(state['ret']))
        await get_params.finish(message='ok~')
       