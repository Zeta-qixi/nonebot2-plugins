from typing import List, Optional, Dict, Any
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

# --- Module Schemas ---
class ModuleCreate(BaseModel):
    id: str
    name: str
    type: str
    remark: Optional[str] = None
    content: Optional[str] = None

class ModuleResponse(ModuleCreate):
    pass

# --- Part Schemas ---
class PartCreate(BaseModel):
    id: str
    name: str
    type: str
    value: str
    remark: Optional[str] = None 

class PartResponse(PartCreate):
    pass

# --- Workspace Schemas ---
class WorkspaceCreate(BaseModel):
   
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True     
    )

    id: str
    name: str
    active_module_ids: List[str]
    active_model_parts: Dict[str, Any]
    engine_params: Dict[str, Any]
    history_strategy: Dict[str, Any]
    slot_values: Optional[Dict[str, Any]] = None
    resolved_system_prompt: Optional[str] = None
    updated_at: Optional[float] = None


class WorkspaceResponse(WorkspaceCreate):
    pass

# --- Chat Schemas ---
class ChatRequest(BaseModel):
    currentConfigId: str
    userInput: str
    chatMessages: List[Dict[str, Any]] = []