import asyncio
import os
import random
import re
import time
from collections import defaultdict
import requests
from nonebot import get_driver, on_command, on_regex
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.event import Event
from nonebot.adapters.onebot.v11.message import Message, MessageSegment
from nonebot.log import logger
from nonebot.typing import T_State
from nonebot.params import State, CommandArg

from PIL import Image

from .Getpic import SetuBot
from .utils import set_random_seed

try:
    master = get_driver().config.master
except:
    master = []
TRAN = {
    '一':1, '二':2, '两':2, '三':3, '四':4, '五':5,
    '六':6,
}
path =os.path.dirname(__file__) + '/data'

## setubot
class setubot(SetuBot):
    def __init__(self):
        super(setubot, self).__init__()
        self.picID_by_user = defaultdict(list)
        self.rank_mode_list = self.get_rank_keys()
        self.user_rank_mode = defaultdict(int)
        self.group_token = {}

    def push_pic_id(self, uid, pid_list):
        self.picID_by_user[int(uid)] = pid_list
        
setubot = setubot()

base_setu        =      on_command('setu',aliases={'Setu', 'SETU', '色图'}, priority=11, block=True)
change_rank_mode =      on_command("setumode", priority=10, block=True) # 优先setu
my_follow        =      on_regex('来(.?)份[涩色瑟]图', block=False)
recall_setu      =      on_regex('^撤回|太[涩色瑟]了', block=False)
r18_switch       =      on_regex("(不可以|强制)色色", block=False)




@base_setu.handle()
async def setu_handle(bot: Bot, event: Event, state: T_State, comman_: Message = CommandArg()):

    uid = event.user_id
    gid = event.group_id
    set_random_seed(uid)
    token_sign = setubot.group_token.get(gid, 'no_r18')
    keyword = setubot.rank_mode_list[setubot.user_rank_mode[uid]]
    comman = str(comman_).rsplit(' ', 1)
    num = 1

    # 变量只有一个 判定是keyword还是num
    if comman[-1].isdigit() and len(comman[-1]) == 1:
        num = int(comman[-1])
        if len(comman) == 2:
            keyword = comman[0]
    else:
        if str(comman_) != '':
            keyword = str(comman_)
    num = 3 if num > 3 else num

    if ret := re.search(r'(画师|作者|搜[索图]|推荐)\s?(.*)', keyword):
        if ret.group(1) == '推荐':
            res, res_data = await setubot.get_setu_recommend(int(ret.group(2)), num, token_sign)
        elif ret.group(1) in ['搜索', '搜图']:
            res, res_data = await setubot.get_setu_by_id(int(ret.group(2)), token_sign)
        else:
            res, res_data = await setubot.get_setu_artist(ret.group(2), num, token_sign)
    else:
        logger.info(f"关键词: {keyword}, token:{token_sign}")
        res, res_data = await setubot.get_setu_base(keyword, num, token_sign)

    state['token_sign'] = token_sign
    state['keyword'] = keyword

    if res == 1000:
        msg_list = []
        for info, pic_path in (res_data):
            msg = await bot.send(event, message = info + MessageSegment.image(f'file://{pic_path}'))
            msg_list.append(msg['message_id'])
        setubot.push_pic_id(uid, msg_list)
    else:
        await send_setu.finish(message = '你🐛的太快啦')

@base_setu.receive()
async def setu_receive(bot: Bot, event: Event, state: T_State):
    if str(event.message) == '不够色':
        res, res_data = await setubot.get_setu_base(state['keyword'], 1, state['token_sign'])
        msg_list = []
        for info, pic_path in (res_data):
            msg = await base_setu.finish(message = info + MessageSegment.image(f'file://{pic_path}'))
            msg_list.append(msg['message_id'])
        setubot.push_pic_id(event.user_id, msg_list)




@recall_setu.handle()
async def _(bot: Bot, event: Event, state: T_State):
    id = event.user_id
    if setubot.picID_by_user[id]:
        for pid in setubot.picID_by_user[id]:
            time.sleep(2)
            await bot.delete_msg(message_id=pid)
        setubot.picID_by_user[id] = []

        dir = path + '/nosese'
        img_src = dir + '/' + random.choice(os.listdir(dir))
        logger.info(img_src)
        await recall_setu.finish(message = MessageSegment.image(f'file://{img_src}'))





@my_follow.handle()
async def my_follow_(bot: Bot, event: Event, state: T_State):
    
    num = str(state['_matched_groups'][0])
    if num:
        num = int(num) if num.isdigit() else  TRAN.get(num)
    else:
        num = 1
    uid = event.user_id
    res, res_data = await setubot.get_follow_setu(num, uid)
    if res == 400:
        await bot.send(event, message = "你的🆔没在列表内登记哦～")

    if res == 1000:
        msg_list = []
        for info, pic_path in (res_data):
            msg = await bot.send(event, message = info + MessageSegment.image(f'file://{pic_path}'))
            msg_list.append(msg['message_id'])
        setubot.push_pic_id(uid, msg_list)




@r18_switch.handle()
async def no_r18_handle(bot: Bot, event: Event, state: T_State):
    gid = event.group_id
    uid = event.user_id

    member_info = await bot.get_group_member_info(group_id=gid, user_id=uid)
    if member_info['role'] == "owner" or member_info['role'] == "admin" or uid in master:

        if str(state['_matched_groups'][0]) == '不可以':
            setubot.group_token[gid] = 'no_r18'
            img_src = path+'/bkyss.png'
        else:
            setubot.group_token[gid] = None
            img_src = path+'/ss.png'
        await r18_switch.finish(message = MessageSegment.image(f'file://{img_src}'))

    else:
        await r18_switch.finish(message = MessageSegment.image(f'你没有发动权限'))




@change_rank_mode.handle()
async def change_rank_mode_handle(bot: Bot, event: Event, state: T_State, mode: Message = CommandArg()):
    mode = str(mode)
    if mode:
        state['mode_index'] = mode
    state['uid'] = event.user_id


mode_info = '要选什么模式呢～\n' + '\n'.join([f"[{index}] {info}" for index, info in enumerate(setubot.rank_mode_list)])

@change_rank_mode.got('mode_index', prompt=mode_info)
async def set_got(bot: Bot, event: Event, state: T_State):

    index = int(str(state['mode_index']))
    setubot.user_rank_mode[int(state['uid'])] = index
    await change_rank_mode.finish(message = "设置成功")
