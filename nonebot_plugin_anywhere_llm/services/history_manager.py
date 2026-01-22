import time
from typing import List, Dict
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import ChatHistory

class HistoryManager:

    @staticmethod
    async def add_message(
        db: AsyncSession, 
        user_id: str, 
        group_id: str, 
        workspace: str, 
        role: str, 
        content: str
    ):
        message = ChatHistory(
            user_id=user_id,
            group_id=group_id,
            workspace=workspace,
            role=role,
            content=content,
            timestamp=time.time()
        )
        db.add(message)
        return message

    @staticmethod
    async def get_context(
        db: AsyncSession, 
        user_id: str, 
        group_id: str, 
        workspace: str, 
        history_cfg: Dict
    ) -> List[Dict[str, str]]:
        
        time_window = history_cfg.get("timeWindowMinutes", 60)
        max_count = history_cfg.get("maxCount", 10)
        cutoff_time = time.time() - (time_window * 60)

        stmt = (
            select(ChatHistory)
            .where(
                ChatHistory.user_id == user_id,
                ChatHistory.group_id == group_id,
                ChatHistory.workspace == workspace,
                ChatHistory.timestamp > cutoff_time
            )
            .order_by(desc(ChatHistory.timestamp)) # 倒序取最新
            .limit(max_count)
        )

        result = await db.execute(stmt)
        messages = result.scalars().all()

        # 反转回正序
        return [{"role": m.role, "content": m.content} for m in reversed(messages)]