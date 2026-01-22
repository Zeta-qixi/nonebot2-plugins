from sqlalchemy.ext.asyncio import AsyncSession
from nonebot.log import logger

from .history_manager import HistoryManager
from .openai_chat import build_cfg_options, call_openai

async def chat_service(
    db: AsyncSession, 
    workspace_name: str,
    prompt: str,
    user_id: str = None,
    group_id: str = None,
) -> str:
    """
    业务逻辑层：包含完整的 查配置 -> 查历史 -> 调API -> 存记录 流程
    """
    try:
        history_context = []
        api_cfg, history_cfg = await build_cfg_options(db, workspace_name)

        if user_id or group_id:
            history_context = await HistoryManager.get_context(
                db, user_id, group_id, workspace_name, history_cfg
            )

        response = await call_openai(api_cfg, prompt, history_context)

        if user_id or group_id:
            await HistoryManager.add_message(
                db, user_id, group_id, workspace_name, "user", prompt
            )
            await HistoryManager.add_message(
                db, user_id, group_id, workspace_name, "assistant", response
            )
            await db.commit()
        return response

    except Exception as e:
        await db.rollback()
        logger.error(f"Chat service error: {e}")
        raise e