"""
自然语言 创建任务
"""
import random


from nonebot import on_message
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import (Message, GroupMessageEvent, MessageEvent, MessageSegment)

from .model import Clock
from .utils import parse_natural_language, get_event_info, message_to_db
from .llm import natural_language_to_task
from .handle import job_handle


natural_language_add_clock = on_message(block=False)


@natural_language_add_clock.handle()
async def _(matcher: Matcher, event: MessageEvent): 
    message = event.get_plaintext()
    # res = await natural_language_to_task(message)
    # cron_expression, content, is_one_time = res['cron'], res['remind'], res['ones']
    content, cron_expression = parse_natural_language(message)
    is_one_time = True
    if content and cron_expression:
        
        data = {
            'id': 0,
            'is_one_time': is_one_time,
            'cron_expression': cron_expression,
            'content': message_to_db(Message(content))
        }

        data['type'], data['group_id'] ,data['user_id'] = get_event_info(event)
        job_handle.add_clock(Clock(data))
        matcher.block = True
        await matcher.finish(message='好的')
    