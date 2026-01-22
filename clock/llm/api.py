
from typing import Optional, Dict
from nonebot import logger

from nonebot import require
simple_chat = require('nonebot_plugin_anywhere_llm').simple_chat

async def decorate_content(content: str) -> Optional[str]:
 
    response = await simple_chat(
        'clock',
        f"事项：{content}",
    )
    return response



async def natural_language_to_task(content: str) -> Dict:
    ...