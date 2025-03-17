# history_manager.py
from nonebot_plugin_orm import Model, get_session
from sqlalchemy import Column, Integer, String, DateTime, Text, Index
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from typing import List, Tuple

class ChatHistory(Model):
    """聊天历史记录模型"""
    __table_args__ = (
        Index("idx_session", "session_id"),  # 创建会话索引
    )
    
    id = Column(Integer, primary_key=True)
    session_id = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.now)

class HistoryManager:
    async def add_record(self, session_id: str, role: str, content: str):
        """添加聊天记录"""
        async with get_session() as db_session:
            db_session.add(ChatHistory(
                session_id=session_id,
                role=role,
                content=content
            ))
            await db_session.commit()

    async def get_history(self, session_id: str, max_turns: int = 5) -> List[Tuple[str, str]]:
        """获取历史对话"""
        async with get_session() as db_session:
            result = await db_session.execute(
                select(ChatHistory)
                .where(ChatHistory.session_id == session_id)
                .order_by(ChatHistory.timestamp.desc())
                .limit(max_turns * 2)
            )
            records = result.scalars().all()
            return [(r.role, r.content) for r in reversed(records)]