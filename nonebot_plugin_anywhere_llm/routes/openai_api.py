from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException
from ..database import get_db_session
from ..services.openai_chat import call_openai, build_cfg_options
from ..schemas import ChatRequest

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("")
async def chat(data: ChatRequest, db: AsyncSession = Depends(get_db_session)):
    """
    FastAPI 原生异步支持。
    去掉了 asyncio.run()，直接 await call_openai。
    """
    if not data.currentConfigId or not data.userInput:
        raise HTTPException(status_code=400, detail="Missing workspaceName or prompt")
    cfg, _ = await build_cfg_options(db, data.currentConfigId) 
    
    try:
        # 直接 await 异步函数
        response = await call_openai(cfg, data.userInput, data.chatMessages)
        return {"text": response}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/health")
async def health_check():
    return {"status": "ok"}