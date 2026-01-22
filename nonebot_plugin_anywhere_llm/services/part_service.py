from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from ..models import ModelPart
from ..schemas import PartCreate


async def create_part(db: AsyncSession, data: PartCreate):
    result = await db.execute(select(ModelPart).where(ModelPart.id == data.id))
    mod = result.scalar_one_or_none()

  
    final_value = data.value
    if not mod:
        part = ModelPart(
            id=data.id,
            name=data.name,
            type=data.type,
            remark=data.remark,
            value=final_value
        )
        db.add(part)
    else:
        mod.name = data.name
        mod.type = data.type
        mod.remark = data.remark
        mod.value = final_value

    try:
        await db.commit()
        await db.refresh(part if not mod else mod)
    except IntegrityError:
        await db.rollback()
        raise ValueError("Part save failed")
    
    return part if not mod else mod

async def delete_part(db: AsyncSession, part_id: str):
    result = await db.execute(select(ModelPart).where(ModelPart.id == part_id))
    part = result.scalar_one_or_none()
    if not part:
        raise ValueError("Part not found")

    try:
        await db.delete(part)
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise ValueError("Part delete failed")

async def get_part(db: AsyncSession, part_id: str) -> ModelPart:
    result = await db.execute(select(ModelPart).where(ModelPart.id == part_id))
    part = result.scalar_one_or_none()
    
    if not part:
        raise ValueError("Part not found")
    
    part.value = part.value
    return part

async def list_parts(db: AsyncSession):
    result = await db.execute(select(ModelPart))
    return result.scalars().all()