from nonebot_plugin_orm import Model
from sqlalchemy import Column, String, Text, JSON, DateTime

class ConversationHistory(Model):
    """对话历史记录存储模型"""
    __table_args__ = {"extend_existing": True}
    
    session_id = Column(String(255), primary_key=True)
    plugin_name = Column(String(50), index=True)
    history = Column(JSON)
    updated_at = Column(DateTime)