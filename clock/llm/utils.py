from datetime import datetime
from pathlib import Path
from typing import Optional, Dict
from nonebot import logger, require
from .prompt import PROMPT, cron_prompt

import locale
import json
locale.setlocale(locale.LC_ALL, 'zh_CN.UTF-8')

LLMParams = require('nonebot_anywhere_llm').LLMParams
LLMService = require('nonebot_anywhere_llm').LLMService
llm_system_time = require('nonebot_anywhere_llm').llm_system_time


clock_llm_params = LLMParams(
    model = 'deepseek-ai/DeepSeek-R1-Distill-Qwen-32B',
    system_prompt=PROMPT,
    temperature=0.5,
    max_tokens=100,
)
llm = LLMService(clock_llm_params)

          
async def decorate_content( content: str) -> Optional[str]:
    try:
        response = await llm.generate(
            prompt = f"当前时间：{llm_system_time()}\n 任务：{content}"
        )
        return response
    except Exception as e:
        logger.error("OpenAI API返回无效响应", repr(e))
        return content


natural_language_to_task_params = LLMParams(
    model = 'deepseek-ai/DeepSeek-R1-Distill-Qwen-32B',
    system_prompt=cron_prompt,
    temperature=0.1,
    max_tokens=2000,
)

async def natural_language_to_task(content: str) -> Dict:
   
    response = await llm.generate(
        prompt = f"{llm_system_time()}\n{content}",
        param = natural_language_to_task_params,
    )
    text = response.split('</think>')[-1]
    text = text.split('```json')[-1].split('```')[0]
    return json.loads(text)
