"""
自然语言 创建任务
"""
import random
import time
from nonebot import on_message
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot import require
from nonebot.adapters.onebot.v11 import (MessageEvent)


llm_chat = require('nonebot_plugin_anywhere_llm').llm_chat



chat = on_message(block=False, priority=99, rule=to_me())
@chat.handle()
async def _(matcher: Matcher, event: MessageEvent): 
    
        response: str = await llm_chat(
            user_id = event.user_id,
            group_id = event.group_id,
            workspace_name = 'chat',
            prompt = event.get_plaintext(),

        )
        if response:
            for r in response.split("\\"):
                r=r.strip()
                if r:
                    time.sleep(len(r) / 12 * random.randint(1,3))
                    await matcher.send(r)