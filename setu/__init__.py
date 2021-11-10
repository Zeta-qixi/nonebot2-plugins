
from nonebot import on_command, get_driver, on_regex
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import Event
from nonebot.adapters.cqhttp.message import Message, MessageSegment
from nonebot.typing import T_State
from nonebot.log import logger
from .utils import set_random_seed
import re
import os
import sys
import requests
import random
import asyncio
import time
from collections import defaultdict
from PIL import Image
sys.path.append(os.path.join(os.path.dirname(__file__)))
from Getpic import SetuBot

try:
    master = get_driver().config.master
except:
    master = []
TRAN = {
    '一':1, '二':2, '两':2, '三':3, '四':4, '五':5,
    '六':6,
}
##变量##
path =os.path.dirname(__file__) + '/data'

## setubot
class setubot(SetuBot):
    def __init__(self):
        super(setubot, self).__init__()
        self.pic_message = defaultdict(list)
        self.group_token = {}

    def push_pic_id(self, uid, pid_list):
        self.pic_message[uid] += pid_list

setubot = setubot()

setu = on_command('setu',aliases={'Setu', 'SETU', '色图'})
@setu.handle()
async def setu_handle(bot: Bot, event: Event, state: T_State):

    uid = event.user_id
    gid = event.group_id
    set_random_seed(uid)
    token_sign = setubot.group_token.get(gid, None)


    comman = str(event.message).rsplit(' ', 1)
    keyword = ''
    num = 1
    # 变量只有一个 判定是keyword还是num
    if comman[-1].isdigit() and len(comman[-1]) == 1:
        num = int(comman[-1])
        if len(comman)>=2:
            keyword = comman[0]
    else:
        keyword = str(event.message)
    num = 3 if num > 3 else num
        
    if ret := re.search(r'(画师|作者|搜[索图]|推荐)\s?(.*)', keyword):
        if ret.group(1) == '推荐':
            res, res_data = await setubot.get_setu_recommend(int(ret.group(2)), num, token_sign)
        elif ret.group(1) in ['搜索', '搜图']:
            res, res_data = await setubot.get_setu_by_id(int(ret.group(2)), token_sign)
        else:
            res, res_data = await setubot.get_setu_artist(ret.group(2), num, token_sign)
    else:
        res, res_data = await setubot.get_setu_base(keyword, num, token_sign)

    if res == 1000:
        msg_list = []
        for info, pic_path in (res_data):
            image = MessageSegment.image(f'file://{pic_path}')
            msg = await bot.send(event, message = info + image)
            msg_list.append(msg['message_id'])
        setubot.push_pic_id(uid, msg_list)

    elif res == 1001:
        msg = '好像不能发送图片了..'
        for url in (res_data):
            msg = f'{msg}\n{url}'
        await bot.send(event, message = msg)
    elif res == 1100:
        await bot.send(event, message = '你🐛的太快啦')
        
recall_setu = on_regex('撤回|太[涩色瑟]了', block=False)
@recall_setu.handle()
async def recall_setu_handle(bot: Bot, event: Event, state: T_State):

    id = event.user_id
    if setubot.pic_message[id]:
        await asyncio.sleep(3)
        for pid in setubot.pic_message[id]:
            await bot.delete_msg(message_id=pid)
            setubot.pic_message[id].remove(pid)

        dir = path + '/nosese'
        img_src = dir + '/' + random.choice(os.listdir(dir))
        await bot.send(event, message = MessageSegment.image(f'file://{img_src}'))


my_follow = on_regex('来(.?)份[涩色瑟]图', block=False)
@my_follow.handle()
async def my_follow_(bot: Bot, event: Event, state: T_State):
    
    num = str(state['_matched_groups'][0])
    num = TRAN.get(num)
    if not num:
        num = int(num) if num.isdigit() else 1

    uid = event.user_id
    res, res_data = await setubot.get_follow_setu(num, uid)
    if res == 400:
        await bot.send(event, message = "你的🆔没在列表内登记哦～")

    if res == 1000:
        msg_list = []
        for info, pic_path in (res_data):
            image = MessageSegment.image(f'file://{pic_path}')
            msg = await bot.send(event, message = info + image)
            msg_list.append(msg['message_id'])
        setubot.push_pic_id(uid, msg_list)

chack_pixiv = on_command("查询个人信息")
@chack_pixiv.handle()
async def chack_handle(bot: Bot, event: Event, state: T_State):
    pass

no_r18_command = on_regex("(不可以|强制)色色", block=False)
@no_r18_command.handle()
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
        await bot.send(event, message = MessageSegment.image(f'file://{img_src}'))

    else:
        await bot.send(event, message = MessageSegment.image(f'你没有发动权限'))