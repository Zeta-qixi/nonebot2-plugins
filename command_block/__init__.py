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

block_dict = defaultdict(list)

block = on_message(block=False, priority=-1)
@block.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    raw_message = str(event.message)
    block.block =  False
    group_id = event.group_id
    for command in block_dict[group_id]:
        if command in raw_message:
            block.stop_propagation(block)
        

set_block = on_regex(r'(关闭|开启|查看)功能(.*)?', block=False)
@set_block.handle()
async def _set_block(bot: Bot, event: GroupMessageEvent, state: T_State):
    action, command = state['_matched_groups']
    user_id = event.user_id
    group_id = event.group_id

    if user_id not in master:
        await set_block.finish(message="?")

    if action == '关闭' and command:
        block_dict[group_id].append(command)
        await set_block.finish(message=f"已关闭「{command}」")

    elif action == '开启' and command:
        block_dict[group_id].remove(command)
        await set_block.finish(message=f"已开启「{command}」")
    else: 
        print(block_dict)
