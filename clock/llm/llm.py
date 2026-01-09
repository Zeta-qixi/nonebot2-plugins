from nonebot import logger, require

require('nonebot_plugin_anywhere_llm')
from nonebot_plugin_anywhere_llm import LLMService, LLMParams



llm = LLMService.load('clock.yaml')
natural_language_to_task_llm = LLMService()
# natural_language_to_task_params = LLMParams(
#     model = 'deepseek-ai/DeepSeek-R1-Distill-Qwen-32B',
#     temperature=0.1,
#     max_tokens=2000,
# )
# natural_language_to_task_llm.config.params = natural_language_to_task_params