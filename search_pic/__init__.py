from . import tool
from nonebot import on_command, get_driver, logger
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.event import Event, GroupMessageEvent
from nonebot.adapters.onebot.v11.message import Message
from nonebot.typing import T_State
from nonebot.params import  CommandArg
import re
try:
    master = get_driver().config.master
except:
    master = []


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
            res = await tool.get_image_data(pic_url)

            for data in res:
                if len(data) > 0:
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