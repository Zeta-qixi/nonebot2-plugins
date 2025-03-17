from openai import APIError, APITimeoutError, AsyncOpenAI, AuthenticationError
from nonebot import get_driver, logger
from typing import Any, Dict, List, Tuple

class OpenAIProvider:
    def __init__(self):
        config = get_driver().config
        self.client = AsyncOpenAI(
            api_key=getattr(config, "openai_api_key", ""),
            base_url=getattr(config, "openai_base_url", "https://api.openai.com/v1")
        )
        self.model = getattr(config, "openai_model", "gpt-3.5-turbo")

    async def generate(self, messages: List[Tuple[str, str]], **kwargs: Any) -> str:
        

        kwargs['model'] =kwargs.get('model', self.model)
        print(messages)
        try:
            response = await self.client.chat.completions.create(
                messages=messages,
                **kwargs,
            )
            return response.choices[0].message.content
        except APITimeoutError as e:
            logger.error(f"API 请求超时: {e}")
            return "⚠️请求超时，请重试"
        except APIError as e:
            logger.error(f"API 错误: {e.status_code} - {e.message}")
            return "⚠️服务暂时不可用"
        except AuthenticationError:
            logger.critical("API 密钥错误")
            return "⚠️服务配置错误"
        except Exception as e:
            logger.error(f"未处理异常: {e}")
            return "⚠️服务内部错误"

