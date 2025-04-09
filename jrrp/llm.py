from nonebot import require
LLMService = require('nonebot_plugin_anywhere_llm').LLMService



llm = LLMService()
llm.config.params.temperature = 0.7
llm.config.messages.system_prompt.template = 'jrrp'
llm.config.params.model = "Qwen/Qwen2.5-7B-Instruct"

async def llm_respone( rp: str) -> str:
    response = await llm.generate(
        f"{rp}/100"
    )
    return response