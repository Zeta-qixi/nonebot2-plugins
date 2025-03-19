# 项目结构 
- 🚀 开箱即用的LLM集成能力 
- 🔧 提供灵活的 config 与 prompt 设置


## todo
- 提供自定义的 history 模块
- 
## 快速使用
```python

llm = require('nonebot_anywhere_llm').llm_sv

test_matcher = on_command("ask")
@test_matcher.handle()
async def handle_ask(event: GroupMessageEvent):  
    
    response = await llm.generate(
        event,
        '返回测试'
    )
    await test_matcher.finish(response)

```

