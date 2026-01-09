from nonebot import require
require('nonebot_plugin_anywhere_llm')
from nonebot_plugin_anywhere_llm import LLMService
def fortune_level(score: int) -> str:
    levels = [
        (15, "大凶"),
        (30, "凶"),
        (50, "小凶"),
        (65, "末吉"),
        (80, "小吉"),
        (90, "吉"),
        (100, "大吉")
    ]

    for threshold, level in levels:
        if score <= threshold:
            return level


llm = LLMService.load('jrrp.yaml')
async def llm_respone( rp: str) -> str:
    response = await llm.generate(
        f"抽签: {fortune_level(rp)}",
        save=True
        
    )
    return response