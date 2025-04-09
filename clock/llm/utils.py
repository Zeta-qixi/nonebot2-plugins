from typing import Optional, Dict
from nonebot import logger, require


require('nonebot_plugin_anywhere_llm')
from nonebot_plugin_anywhere_llm import LLMService



llm = LLMService.from_yaml('clock.yaml')

async def decorate_content( content: str) -> Optional[str]:
    try:
        response = await llm.generate(
            prompt = f"任务：{content}"
        )
        return response
    except Exception as e:
        logger.error("OpenAI API返回无效响应", repr(e))
        return content


natural_language_to_task_llm = LLMService()
# natural_language_to_task_params = LLMParams(
#     model = 'deepseek-ai/DeepSeek-R1-Distill-Qwen-32B',
#     temperature=0.1,
#     max_tokens=2000,
# )

async def natural_language_to_task(content: str) -> Dict:
   
    ...
