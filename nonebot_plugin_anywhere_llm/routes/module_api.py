from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ..database import get_db_session
from ..schemas import ModuleCreate, ModuleResponse
from ..services import module_service

router = APIRouter(prefix="/modules", tags=["Modules"])

@router.post("", response_model=dict)
async def save(data: ModuleCreate, db: AsyncSession = Depends(get_db_session)):
    try:
        mod = await module_service.create_module(db, data)
        return {"id": mod.id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("", response_model=List[ModuleResponse])
async def get_modules(db: AsyncSession = Depends(get_db_session)):
    modules = await module_service.list_modules(db)
    return modules 

@router.delete("/{module_id}", status_code=204)
async def delete(module_id: str, db: AsyncSession = Depends(get_db_session)):
    try:
        await module_service.delete_module(db, module_id)
        return
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))