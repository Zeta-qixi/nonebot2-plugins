from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import plugin_config




# 构造数据库 URL (使用 aiosqlite 驱动)

DB_URL = f"sqlite+aiosqlite:///{plugin_config.db_path}"

engine = create_async_engine(DB_URL, echo=False)

# 创建异步 Session 工厂
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


Base = declarative_base()

async def init_db():
    """初始化数据库表结构"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# 依赖注入辅助函数 (如果使用 Fastapi/Depends 风格)
async def get_db_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session