from nonebot import require
from typing import Dict, List, Optional, Union
from .provider import OpenAIProvider
# from .history_manager import HistoryManager
from .prompt import SystemTemplate, PromptTemplate
from nonebot.adapters import Event


# LLMService.py
class LLMService:
    def __init__(self):
        self.provider = OpenAIProvider()
        self.history_mgr = None


    async def generate(
        self,
        messages: Union[str, List, Dict],
        **kwargs
    ) -> str:
        if isinstance(messages, str):
            messages = PromptTemplate.messgae(messages, 'user')
        if isinstance(messages, Dict):
            messages = [messages]
            
        response = await self.provider.generate(
            messages = messages,
            **kwargs
        )
        return response

