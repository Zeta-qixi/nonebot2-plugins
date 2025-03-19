"""
自然语言 创建闹钟
"""

from .scheduler import myhandle
from nonebot import on_message
from nonebot.matcher import Matcher

from nonebot.adapters.onebot.v11 import (Message, GroupMessageEvent, MessageEvent, MessageSegment)
from .uilts import parse_natural_language, get_event_info


natural_language_add_clock = on_message(block=False)


@natural_language_add_clock.handle()
async def _(matcher: Matcher, event: MessageEvent): 

    content, cron_expression = parse_natural_language(event.get_plaintext())
    if content and cron_expression:
        
        data = {
            'id': 0,
            'is_one_time': True,
            'cron_expression': cron_expression,
            'content': message_to_db(Message(content))
        }
        data['type'], data['group_id'] ,data['user_id'] = get_event_info(event)
        add_clock(myhandle, **data)
        tmp_respone = ['嗯','好的','明白了，我会记住的。','知道啦']
        await matcher.finish(message=random.choice(tmp_respone))
    
