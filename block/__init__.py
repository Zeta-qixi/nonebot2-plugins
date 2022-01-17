import json
import os
from collections import defaultdict
from nonebot import on_message, on_regex, get_driver
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import GroupMessageEvent
from nonebot.rule import to_me
from nonebot.typing import T_State

try:
    master = get_driver().config.master
except:
    master = []



PATH = os.path.dirname(__file__)+'/data.json'
try:
    with open(PATH) as f:
        data = json.load(f)
    block_dict = defaultdict(list, data)
except:
    with open(PATH, 'w+') as f:
        f.write('{}')
    block_dict = defaultdict(list)

def save_to_file():
    with open(PATH, 'w+') as f :
            tojson = json.dumps(block_dict,sort_keys=True, ensure_ascii=False, indent=4,separators=(',',': '))
            f.write(tojson)

block = on_message(block=False, priority=-1)
@block.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    raw_message = str(event.message)
    block.block =  False
    group_id = str(event.group_id)
    for command in block_dict[group_id]:
        if(raw_message.startswith(command)):
            block.stop_propagation(block)
        

set_block = on_regex(r'(关闭命令|开启命令|不再回答)(.*)?', priority=-2)
@set_block.handle()
async def _set_block(bot: Bot, event: GroupMessageEvent, state: T_State):
    action, command = state['_matched_groups']
    user_id = event.user_id
    group_id = str(event.group_id)

    if user_id not in master:
        await set_block.finish(message="?")

    if action in ['关闭命令','不再回答'] and command:
        block_dict[group_id].append(command)
        await set_block.send(message=f"{action}「{command}」")

    elif action == '开启命令' and command:
        if command in block_dict[group_id]:
            block_dict[group_id].remove(command)
            await set_block.send(message=f"{action}「{command}」")
    else: 
        print(block_dict)

    save_to_file()
