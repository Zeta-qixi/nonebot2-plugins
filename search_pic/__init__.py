import re
import aiohttp
import asyncio
from nonebot import get_driver, logger, on_command
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.event import Event, GroupMessageEvent
from nonebot.adapters.onebot.v11.message import Message
from nonebot.params import CommandArg
from nonebot.typing import T_State

from .tool import from_ascii2d, from_saucenao


search = on_command('搜图')
@search.handle()
async def search_handle(bot: Bot, event: Event, state: T_State, msg: Message = CommandArg()):
    
    if event.reply:
        state['ret'] = event.reply.message["image"]
    elif msg:
        state['ret'] = msg

@search.got('ret', prompt='图呢')
async def search_got(bot: Bot, event: GroupMessageEvent, state: T_State):

    for msg in state['ret']:

        if msg.type == 'image':
            await bot.send(event, message='处理图片...')
            pic_url = msg.data['url']
            logger.info(f'开始搜图{pic_url}')
            
            async with aiohttp.ClientSession() as s:
                tasks = [asyncio.create_task(func(s, pic_url)) for func in [from_saucenao, from_ascii2d]]
                done, _ = await asyncio.wait(tasks)
                for i in done:
                    data = i.result()
                    if data:
                        await send_forward_msg_group(bot, event, "搜图" ,data)

        else:
            await search.finish('不搜啦、')



# 合并消息
async def send_forward_msg_group(
        bot: Bot,
        event: GroupMessageEvent,
        name: str,
        msgs: [],
):
    def to_json(msg):
        return {"type": "node", "data": {"name": name, "uin": bot.self_id, "content": msg}}

    messages = [to_json(msg) for msg in msgs]
    await bot.call_api(
        "send_group_forward_msg", group_id=event.group_id, messages=messages
    )
