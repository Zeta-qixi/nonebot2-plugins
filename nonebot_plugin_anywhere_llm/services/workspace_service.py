import time
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from nonebot.log import logger

from ..models import WorkspaceConfig
from ..schemas import WorkspaceCreate

async def list_workspaces(db: AsyncSession):
   
    result = await db.execute(select(WorkspaceConfig))
    return result.scalars().all()

async def select_workspace(db: AsyncSession, workspace_sp: str) -> WorkspaceConfig:

    result = await db.execute(select(WorkspaceConfig).where(WorkspaceConfig.id == workspace_sp))
    config = result.scalar_one_or_none()
    if not config:
        result = await db.execute(select(WorkspaceConfig).where(WorkspaceConfig.name == workspace_sp))
        config = result.scalar_one_or_none()
        
    return config

async def save_workspace(db: AsyncSession, config: WorkspaceCreate):
    
    result = await db.execute(select(WorkspaceConfig).where(WorkspaceConfig.id == config.id))
    ws = result.scalar_one_or_none()
    updated_at_val = time.time()
  
    if not ws:
        ws = WorkspaceConfig(
            id=config.id,
            name=config.name,
            active_module_ids=config.active_module_ids,
            active_model_parts=config.active_model_parts,
            engine_params=config.engine_params,
            history_strategy=config.history_strategy,
            slot_values=config.slot_values,
            resolved_system_prompt=config.resolved_system_prompt,
            updated_at=updated_at_val,
        )
        db.add(ws)
    else:
        ws.name = config.name
        ws.active_module_ids = config.active_module_ids
        ws.active_model_parts = config.active_model_parts
        ws.engine_params = config.engine_params
        ws.history_strategy = config.history_strategy
        ws.slot_values = config.slot_values
        ws.resolved_system_prompt = config.resolved_system_prompt
        ws.updated_at = updated_at_val

    try:
        await db.commit()
        await db.refresh(ws)
    except IntegrityError as e:
        print(e)
        await db.rollback()
        raise ValueError("Workspace save failed")

    return ws

async def delete_workspace(db: AsyncSession, workspace_id: str) -> bool:
    result = await db.execute(select(WorkspaceConfig).where(WorkspaceConfig.id == workspace_id))
    ws = result.scalar_one_or_none()
    
    if not ws:
        return False

    await db.delete(ws)
    await db.commit()
    return True