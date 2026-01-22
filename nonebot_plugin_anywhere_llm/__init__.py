from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from nonebot import get_driver, logger, get_app
from nonebot.plugin import PluginMetadata

from .config import  Config
from .database import init_db, AsyncSessionLocal
from .routes import module_api, part_api, workspace_api, openai_api

__plugin_meta__ = PluginMetadata(
    name="nonebot_plugin_anywhere_llm",
    description="大模型Prompt管理器",
    usage=("通过网页组合prompt\n"
        "通过指定模板名称使用组合的prompt与model配置"),
    config=Config,
)

# 挂载前端网页
app = get_app()
app.include_router(module_api.router, prefix="/llm-bridge/api")
app.include_router(part_api.router, prefix="/llm-bridge/api")
app.include_router(workspace_api.router, prefix="/llm-bridge/api")
app.include_router(openai_api.router, prefix="/llm-bridge/api")
PLUGIN_DIR = Path(__file__).parent
DIST_DIR = PLUGIN_DIR / "web" / "dist"
app.mount("/assets", StaticFiles(directory=DIST_DIR / "assets"), name="assets")
@app.get("/llm-bridge")
async def serve_spa():
    index_path = DIST_DIR / "index.html"
    return HTMLResponse(index_path.read_text(encoding='utf-8'))


# 自动建表
driver = get_driver()
@driver.on_startup
async def _():
    logger.info("Initializing LLM History Database...")
    await init_db()




# --- 对外核心接口 ---
from .services.bridge import chat_service

async def llm_chat(
    workspace_name: str, 
    prompt: str,
    user_id: str = None, 
    group_id: str = None, 
) -> str:
    """
    调用接口, 保存历史对话
    """
    async with AsyncSessionLocal() as db:
        try:
            response = await chat_service(
                db=db, 
                user_id=user_id, 
                group_id=group_id, 
                workspace_name=workspace_name, 
                prompt=prompt
            )
            return response
        except Exception as e:
            raise e
            

async def simple_chat(
    workspace_name: str, 
    prompt: str
) -> str:
    """
    简易调用，不保存对话
    """
    return await llm_chat(workspace_name, prompt)