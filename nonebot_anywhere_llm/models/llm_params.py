from typing import Dict, List, Any
class LLMParams:
    """模型基础参数配置"""
    def __init__(
        self,
        model: str = "Qwen/Qwen2.5-7B-Instruct",
        temperature: float = 0.7,
        max_tokens: int = 2000,
        # top_p: float = 1.0,
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0,
        system_prompt: str = None
    ):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.system_prompt = system_prompt
        
    def get_system_prompt(self) -> List[Any]:
        if self.system_prompt:
            return [{"role": "system", "content": self.system_prompt}]