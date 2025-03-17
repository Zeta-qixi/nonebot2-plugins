from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="nonebot-anywhere-llm",
    description="提供 LLM 访问能力的插件，支持多种模型和自定义 Prompt",
    usage="直接调用 `get_llm_response` 进行 LLM 交互",
)


from .llm_service import LLMService
from .prompt import SystemTemplate, PromptTemplate

llm_sv = LLMService()