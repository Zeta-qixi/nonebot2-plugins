from .detection import IMAGE_PATH, get_detection_res

from nonebot import on_command
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import Event, GroupMessageEvent,MessageEvent
from nonebot.adapters.cqhttp.message import MessageSegment
from nonebot.typing import T_State
from nonebot import require, logger

face_ = on_command("检测")

@face_.handle()
async def add_handle(bot: Bot, event: Event, state: T_State):
    pass
    for msg in event.get_message():
        if msg.type == 'image':
            url = msg.data['url']

        if msg.type == 'text':
             qq = msg.data['text']
             url = f'http://q1.qlogo.cn/g?b=qq&nk={qq}&s=160'
             print(url)
            

        if(get_detection_res(url = url)):
            logger.info("检测完成")
            msg_pic = MessageSegment.image(f"file://{IMAGE_PATH}")
            await face_.finish(message=msg_pic)
        else:
            logger.info("检测不到东西噢")