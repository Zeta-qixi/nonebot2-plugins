"""
自然语言 创建任务
"""
import random
import time
from nonebot import on_message
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot import require
from nonebot.adapters.onebot.v11 import (Message, PrivateMessageEvent, GroupMessageEvent, MessageEvent, MessageSegment)

require('nonebot_plugin_anywhere_llm')
from nonebot_plugin_anywhere_llm import LLMService

llm = LLMService.load('chat.yaml')


chat = on_message(block=False, priority=99)
@chat.handle()
async def _(matcher: Matcher, event: PrivateMessageEvent): 
    
    response: str = await llm.generate(
        event.get_plaintext(),
        event=event,
        save=True,
    )
    if response:
        for r in response.split("\\"):
            r=r.strip()
            if r:
                time.sleep(len(r) / 12 * random.randint(1,3))
                await matcher.send(r)