from nonebot import get_driver, require
from typing import Dict, List, Optional, Union
from nonebot.adapters.onebot.v11 import MessageEvent
from .provider import OpenAIProvider
from .history_manager import SQLiteHistoryManager
from .models import LLMParams

# LLMService.py


class LLMService:
    def __init__(self, llm_param = None, history_mgr= None):
        
        self.provider = OpenAIProvider()
        self.param = llm_param or LLMParams()
        self.history_mgr = history_mgr or SQLiteHistoryManager()


    async def generate(
        self,
        event: MessageEvent,
        prompt: str,
        use_histroy: bool = False,
        histroy_length: int = 10
    ) -> str:

        
        messages = self.param.get_system_prompt()
        session_id = event.get_session_id()
        if use_histroy:
            histroy = await self.history_mgr.get_history(session_id, length=histroy_length)
            messages.extend(histroy)
        messages.extend({"role": 'user', 'content': prompt})
        
        
        response = await self.provider.generate(
            messages = messages,
            params = params
        )
        if use_histroy:
            await self.history_mgr.save_message(session_id, 'user', prompt)
            await self.history_mgr.save_message(session_id, 'system', response)
            
        return response

