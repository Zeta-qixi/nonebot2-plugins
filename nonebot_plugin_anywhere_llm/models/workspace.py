from sqlalchemy import Column, String, Text, JSON, BigInteger
from ..database import Base

class WorkspaceConfig(Base):
    __tablename__ = "workspace_configs"
    id = Column(String(64), primary_key=True)
    name = Column(String(100), nullable=False)
    
    # 在 SQLAlchemy 中存储列表/字典通常用 JSON 类型
    active_module_ids = Column(JSON, nullable=True)
    active_model_parts = Column(JSON, nullable=True)
    engine_params = Column(JSON, nullable=True)
    history_strategy = Column(JSON, nullable=True)
    slot_values = Column(JSON, nullable=True)
    resolved_system_prompt = Column(Text, nullable=True)
    
    updated_at = Column(BigInteger, nullable=True)