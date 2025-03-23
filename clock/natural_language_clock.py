"""
自然语言 创建任务
"""
import random

from nonebot import on_message
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import (Message, GroupMessageEvent, MessageEvent, MessageSegment)

from .utils import parse_natural_language, get_event_info, message_to_db
from .llm import natural_language_to_task
from .scheduler import myhandle
from .handle.job import add_clock

natural_language_add_clock = on_message(block=False, rule=to_me())


@natural_language_add_clock.handle()
async def _(matcher: Matcher, event: MessageEvent): 

    message = event.get_plaintext()
    for i in ['提醒','叫','让','记得','准备']: # 防止无关聊天调用方法
        if i in message:
            
            try:
                res = await natural_language_to_task(message)
                cron_expression, content, is_one_time = res['cron'], res['remind'], res['ones']
            except:
                
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
                add_clock(myhandle, **data)
                tmp_respone = ['嗯','好的','明白了，我会记住的。','知道啦']
                await matcher.finish(message=random.choice(tmp_respone))
            