from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ..database import get_db_session
from ..schemas import PartCreate, PartResponse
from ..services import part_service

router = APIRouter(prefix="/parts", tags=["Parts"])

@router.post("", response_model=dict)
async def create(data: PartCreate, db: AsyncSession = Depends(get_db_session)):
    try:
        part = await part_service.create_part(db, data)
        return {"id": part.id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("", response_model=List[PartResponse])
async def list_parts(db: AsyncSession = Depends(get_db_session)):
    parts = await part_service.list_parts(db)
    # 构造返回列表，处理脱敏
    results = []
    for p in parts:
        val = "******" if p.type == "TOKEN" else p.value
        results.append(PartResponse(id=p.id, name=p.name, type=p.type, value=val, remark=p.remark))
    return results

@router.delete("/{part_id}", status_code=204)
async def delete(part_id: str, db: AsyncSession = Depends(get_db_session)):
    try:
        await part_service.delete_part(db, part_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))