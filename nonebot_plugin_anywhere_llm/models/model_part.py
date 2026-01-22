from sqlalchemy import Column, String, Text, DateTime, JSON, func
from ..database import Base

class ModelPart(Base):
    __tablename__ = "model_parts"
    id = Column(String(64), primary_key=True)
    name = Column(String(100), nullable=False)
    type = Column(String(32), nullable=False)
    value = Column(Text, nullable=False)
    remark = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())




