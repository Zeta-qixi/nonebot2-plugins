from .detection import IMAGE_PATH, get_detection_res

from nonebot import on_command
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import Event, GroupMessageEvent,MessageEvent
from nonebot.adapters.cqhttp.message import MessageSegment, Message
from nonebot.typing import T_State
from nonebot import require, logger

face_ = on_command("检测")

@face_.handle()
async def add_handle(bot: Bot, event: Event, state: T_State):
  
    if (msg:=str(event.get_message())) != '':
        state['url'] = msg

        

@face_.got("url", "图呢")
async def add_handle(bot: Bot, event: Event, state: T_State):
        for msg in Message(state['url']):
            if msg.type == 'image':
                state['url'] = msg.data['url']

            if msg.type == 'text':
                qq = msg.data['text']
                state['url'] = f'http://q1.qlogo.cn/g?b=qq&nk={qq}&s=160'
        
        logger.info('get url', state['url'])

        if(get_detection_res(url = state['url'])):
            logger.info("检测完成")
            msg_pic = MessageSegment.image(f"file://{IMAGE_PATH}")
            await face_.finish(message=msg_pic)
        else:
            await face_.finish(message="检测不到东西噢～")
            logger.info("检测不到东西噢")