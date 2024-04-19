import asyncio
import os
import random
import re
import time
from typing import List, Union
from collections import defaultdict

from nonebot import  get_driver, on_command, on_regex
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.event import Event, GroupMessageEvent
from nonebot.adapters.onebot.v11.message import Message, MessageSegment
from nonebot.log import logger
from nonebot.params import CommandArg
from nonebot.typing import T_State

from .Getpic import SetuBot # type: ignore

master = getattr(get_driver().config,'master',[])

## setubot
class SetuBot(SetuBot):
    def __init__(self):

        super(SetuBot, self).__init__()
        self.rank_mode_list = self.get_rank_keys()
        self.user_rank_mode = defaultdict(int)
        self.group_token = {}

        
setubot = SetuBot()

base_setu        =      on_command('setu',aliases={'Setu', 'SETU', '色图'}, priority=11, block=True)
change_rank_mode =      on_command("setumode", priority=10, block=True) # 优先setu

my_follow        =      on_regex('来(.?)份[涩色瑟]图', block=False)
recall_setu      =      on_regex('^撤回|太[涩色瑟]了', block=False)
r18_switch       =      on_regex("(不可以|强制)色色", block=False)



@base_setu.handle()
async def setu_handle(bot: Bot, event: GroupMessageEvent, state: T_State, keyword: Message = CommandArg()):

    num = 1
    keyword = str(keyword)
    await setubot.set_token(uid=event.get_user_id(), gid = str(event.group_id))
    if ret := re.search(r'(画师|作者|搜[索图])\s?(.*)', keyword):
        keyword = ret.group(2).strip()
        if ret.group(1) == '推荐':
            res_data = await setubot.get_setu_recommend(int(keyword), num)
        elif ret.group(1) in ['搜索', '搜图']:
            res_data = await setubot.get_setu_by_id(int(keyword))
        else:
            res_data = await setubot.get_setu_artist(keyword, num)
    else:
        if setubot.is_private:
            res_data = await setubot.get_follow_setu(num)
        else:
            res_data = await setubot.get_setu_base(keyword, num)
    logger.info(keyword)
    if res_data:
        msgs = []
        for info, pic_path in (res_data):
            msgs += (MessageSegment.text(info) + MessageSegment.image(f'base64://{pic_path}'))
        msg_id = await send_forward_msg_group(bot, event, "setubot", msgs)




@recall_setu.handle()
async def _(bot: Bot, event: Event, state: T_State):
    ...


@r18_switch.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    ...

@change_rank_mode.handle()
async def _( event: GroupMessageEvent, state: T_State, mode: str = str(CommandArg())):
   
    if mode:
        state['mode_index'] = mode
    state['uid'] = event.user_id


@change_rank_mode.got('mode_index', prompt='要选什么模式呢～\n' + '\n'.join([f"[{index}] {info}" for index, info in enumerate(setubot.rank_mode_list)]))
async def _( event: GroupMessageEvent, state: T_State):

    index = int(str(state['mode_index']))
    setubot.user_rank_mode[int(state['uid'])] = index
    
    await change_rank_mode.finish(message = "设置成功")


# 合并消息
async def send_forward_msg_group(
        bot: Bot,
        event: GroupMessageEvent,
        name: str,
        msgs: List,
):
    def to_json(msg):
        return {"type": "node", "data": {"name": name, "uin": bot.self_id, "content": msg}}

    messages = [to_json(msg) for msg in msgs]
    uid = await bot.call_api(
        "send_group_forward_msg", group_id=event.group_id, messages=messages
    )
    return uid['message_id']
