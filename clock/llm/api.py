from .llm import *
from typing import Optional, Dict
from nonebot import logger

async def decorate_content( content: str) -> Optional[str]:
    try:
        response = await llm.generate(
            f"事项：{content}",
        )
        return response
    except Exception as e:
        logger.error(str(e))
        return content.strip()


async def natural_language_to_task(content: str) -> Dict:
    ...