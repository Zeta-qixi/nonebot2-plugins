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
        intput='返回测试'
    )
    await test_matcher.finish(response)

```

## 使用prompt模版
```python
PromptTemplate = require('nonebot_anywhere_llm').PromptTemplate
SystemTemplate = require('nonebot_anywhere_llm').SystemTemplate

my_prompt_template = PromptTemplate("""
System: 请遵守以下规则：
{text} 用户提问时请始终用中文回答""")

sys_prompt_template = SystemTemplate('prompt.txt')

response = await llm.generate(
        system_prmompt = sys_prompt_template.render()
        intput = my_prompt_template.render({"text" : '你好'})
        temperature=0.5,
    )
```