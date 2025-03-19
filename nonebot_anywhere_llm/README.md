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

### 用例
```

my_params = LLMParams(
    model= "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",
)
llm = LLMService(my_params)

test = on_command("test")
@test.handle()
async def handle_ask(matcher: Matcher, event: GroupMessageEvent):  
    res = await llm.generate('回复测试')
    await matcher.finish(res)
    
```