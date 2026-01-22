"""
Nonebot 频繁使用的聊天历史记录表, 单独使用异步 SQLAlchemy 进行操作
"""

from sqlalchemy import Column, Integer, String, Text, Float, Index
from ..database import Base
import time

class ChatHistory(Base):
    __tablename__ = "message_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(64), nullable=False)
    group_id = Column(String(64), nullable=False)
    workspace = Column(String(100), nullable=False)
    
    # role: "user" / "assistant"
    role = Column(String(20), nullable=False)
    content = Column(Text, nullable=False)
    
    # 使用 timestamp float 方便计算
    timestamp = Column(Float, default=time.time)

    # 联合索引优化查询速度
    __table_args__ = (
        Index('idx_chat_query', 'group_id', 'user_id', 'workspace', 'timestamp'),
    )

    def to_dict(self):
        return {"role": self.role, "content": self.content}