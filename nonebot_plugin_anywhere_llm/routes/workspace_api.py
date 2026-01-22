from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any

from nonebot.log import logger
from ..database import get_db_session
from ..schemas import WorkspaceCreate, WorkspaceResponse
from ..services import workspace_service

router = APIRouter(prefix="/workspaces", tags=["Workspaces"])

@router.get("", response_model=List[WorkspaceResponse])
async def list_all(db: AsyncSession = Depends(get_db_session)):
    workspaces = await workspace_service.list_workspaces(db)
    return [
        {
            "id": w.id,
            "name": w.name,
            "activeModuleIds": w.active_module_ids,
            "activeModelParts": w.active_model_parts,
            "engineParams": w.engine_params,
            "historyStrategy": w.history_strategy,
            "slotValues": w.slot_values,
            "updatedAt": w.updated_at if w.updated_at else None, 
        }
        for w in workspaces
    ]

@router.post("")
async def save(data: WorkspaceCreate, db: AsyncSession = Depends(get_db_session)):
  
    try:
        ws = await workspace_service.save_workspace(db, data)
        return {"id": ws.id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{id}")
async def delete(id: str, db: AsyncSession = Depends(get_db_session)):
    success = await workspace_service.delete_workspace(db, id)
    return {"success": success}