from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from ..models import Module
from ..schemas import ModuleCreate

async def list_modules(db: AsyncSession) -> List[Module]:
    result = await db.execute(select(Module).order_by(Module.created_at.desc()))
    return result.scalars().all()


async def create_module(db: AsyncSession, data: ModuleCreate):
    # 查询是否存在
    result = await db.execute(select(Module).where(Module.id == data.id))
    mod = result.scalar_one_or_none()

    if not mod:
        mod = Module(
            id=data.id,
            name=data.name,
            type=data.type,
            content=data.content,
            remark=data.remark
        )
        db.add(mod)
    else:
        mod.name = data.name
        mod.type = data.type
        mod.content = data.content
        mod.remark = data.remark

    try:
        await db.commit()
        await db.refresh(mod) # 刷新以获取最新状态
    except IntegrityError:
        await db.rollback()
        raise ValueError("Module save failed")

    return mod

async def delete_module(db: AsyncSession, module_id: str):
    result = await db.execute(select(Module).where(Module.id == module_id))
    mod = result.scalar_one_or_none()
    
    if not mod:
        raise ValueError("Module not found")

    try:
        await db.delete(mod)
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise ValueError("Module delete failed")