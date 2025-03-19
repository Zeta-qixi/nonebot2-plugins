# nonebot2的插件库
> 基于 nonebot-anywhere-llm ，全面接入大模型的插件，具体功能到插件中看 对应

```
nonebot_anywhere_llm
├── models                # 模型类
│   ├── __init__.py     
│   ├── llm_params.py     # 参数参数，定义推理的各项参数
├── provider              # 处理不同LLM提供商的接口及其实现
│   ├── __init__.py
│   ├── interface.py
│   ├── openai.py
├── prompt.py
├── history_manager.py    # 上下文管理器，以 event.get_session_id 作为索引
├── llm_service.py        # 核心服务类，整合各部分功能，与LLMs交互处理请求和响应
├── readme.md
└── __init__.py

```

## OSCS
[![OSCS Status](https://www.oscs1024.com/platform/badge/Zeta-qixi/nonebot2-plugins.svg?size=large)](https://www.oscs1024.com/project/Zeta-qixi/nonebot2-plugins?ref=badge_large)  

 
## 基础配置
### 大模型基础配置
```
OPENAI_API_KEY=""
OPENAI_MODEL=""
OPENAI_BASE_URL=""  

```

