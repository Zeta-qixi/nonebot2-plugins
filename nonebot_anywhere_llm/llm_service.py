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
        prompt: str,
        param: LLMParams = None,
        session_id: str = None,
        event: MessageEvent = None,
        use_histroy: bool = False,
        histroy_length: int = 10
    ) -> str:

        self.param = param or self.param
        messages = self.param.get_system_prompt() or []

        if use_histroy:
            if (session_id is None or session_id.strip() == '') and event is None:
                raise ValueError("当use_history为True时, session_id和event不能同时为空")
            session_id = session_id or event.get_session_id()
            histroy = await self.history_mgr.get_history(session_id, length=histroy_length)
            messages.extend(histroy)
            
        messages.append({"role": 'user', 'content': prompt})
        
        response = await self.provider.generate(
            messages = messages,
            params = self.param
        )
        if use_histroy:
            await self.history_mgr.save_message(session_id, 'user', prompt)
            await self.history_mgr.save_message(session_id, 'system', response)
            
        return response

