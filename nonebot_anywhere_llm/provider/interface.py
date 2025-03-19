from abc import ABC, abstractmethod
from typing import Any, List, Tuple

class BaseLLMProvider(ABC):
    @abstractmethod
    async def generate(self, messages: List[Tuple[str, str]], **kwargs: Any) -> str:
        pass