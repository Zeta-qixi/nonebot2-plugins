from datetime import datetime
from pathlib import Path
from typing import Optional
from nonebot import logger, require
from .prompt import PROMPT, Reminder
import locale
import json
locale.setlocale(locale.LC_ALL, 'zh_CN.UTF-8')

LLMParams = require('nonebot_anywhere_llm').LLMParams
LLMService = require('nonebot_anywhere_llm').LLMService

clock_llm_params = LLMParams(
    model = 'deepseek-ai/DeepSeek-R1-Distill-Qwen-32B',
    system_prompt=PROMPT,
    temperature=0.5,
    max_tokens=100,
)

llm = LLMService(clock_llm_params)


SEASON = [0, '冬', '冬', '春', '春', '春', '夏', '夏', '夏', '秋', '秋', '秋', '冬']

def llm_system_time():
    now = datetime.now()
    formatted_date = now.strftime("%D，%H:%M，%A ") + SEASON[now.month]
    return formatted_date           
          
async def decorate_content( content: str) -> Optional[str]:

    try:
        response = await llm.generate(
            prompt = f"当前时间：{llm_system_time()}\n 任务：{content}"
        )
        return response
    except:
        logger.warning("OpenAI API返回无效响应")
        return content




# async def decorate_content( content: str) -> Optional[str]:
#     text = text.split('</think>')[-1].split('```json')[-1].rsplit('```')[0]
#     json.loads(json_str)