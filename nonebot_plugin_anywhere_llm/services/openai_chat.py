from nonebot.log import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

import re
from typing import Dict, Set, List, Any

from .workspace_service import select_workspace
from ..schemas import WorkspaceCreate
from .part_service import get_part
from .module_service import list_modules
from openai import AsyncOpenAI
from ..models import Module




async def build_cfg_options(db: AsyncSession, workspace_sp: str) -> tuple[dict, dict]:
    """
    workspace_sp: workspace id or name
    return: (cfg_options, history_cfg)
    """
    workspace = await select_workspace(db, workspace_sp)
    if not workspace:
        raise ValueError(f"Workspace not found: {workspace_sp}")

    # model parts
    api_key = await get_part(db, workspace.active_model_parts["TOKEN"])
    model = await get_part(db, workspace.active_model_parts["MODEL_NAME"])
    base_url = await get_part(db, workspace.active_model_parts.get("URL"))
    
    cfg = {}
    cfg['temperature'] = workspace.engine_params.get('temperature', None)
    cfg['maxOutputTokens'] = workspace.engine_params.get('maxOutputTokens', None)
    cfg['top_p'] = workspace.engine_params.get('TopP', None)
    cfg['frequencyPenalty'] = workspace.engine_params.get('frequencyPenalty', None)
    cfg['presencePenalty'] = workspace.engine_params.get('presencePenalty', None)


    cfg['api_key'] = api_key.value
    cfg['model'] = model.value  
    cfg['base_url'] = base_url.value
    cfg['resolved_system_prompt'] = workspace.resolved_system_prompt
    history_cfg = {
        "timeWindowMinutes": workspace.history_strategy['timeWindowMinutes'],
        "maxCount": workspace.history_strategy['maxCount']
    }

    return cfg, history_cfg





SLOT_PATTERN = re.compile(r"{{(.*?)}}")


async def build_prompt(db: AsyncSession, workspace: WorkspaceCreate) -> str:
    # 1. 加载所有激活模块

    modules = await list_modules(db)

    module_map: Dict[str, Module] = {m.id: m for m in modules}
    slot_values: Dict[str, Any] = workspace.slot_values or {}

    # 2. 解析函数
    def resolve_content(module: Module, visited: Set[str]) -> str:


        visited = set(visited)
        visited.add(module.id)

        text = module.content or ""
        logger.info(slot_values)
        for slot_name in SLOT_PATTERN.findall(text):
            logger.info(slot_name)
            placeholder = f"{{{{{slot_name}}}}}"
            slot_key = f"{module.id}_{slot_name}"
            slot_entry = slot_values.get(slot_key)
            logger.info(slot_entry)
            replacement = ''

            # slot 引用另一个模块
            if isinstance(slot_entry, dict):
                linked_id = slot_entry.get("moduleId")
                linked_module = module_map.get(linked_id)
                if linked_module:
                    replacement = resolve_content(linked_module, visited)

            # slot 是字符串（兜底支持）
            elif isinstance(slot_entry, str) and slot_entry.strip():
                replacement = slot_entry

            text = text.replace(placeholder, replacement)

        return text

    # 3. 按顺序构建最终 prompt
    parts: List[str] = []
    for module_id in workspace.active_module_ids:
        module = module_map.get(module_id)
        if module:
            parts.append(resolve_content(module, set()))

    return "\n\n".join(parts)




async def call_openai(cfg: str, prompt: str, history: list = []) -> str:
    """
    cfg: model config dict
    prompt: user current prompt
    history: list of {"role": "user"/"assistant", "content": "..."}
    """


    client = AsyncOpenAI(
        api_key=cfg['api_key'],
        base_url=cfg['base_url']
    )
    response = await client.chat.completions.create(
        model=cfg['model'],
        messages=[ 
            {"role": "system", "content": cfg['resolved_system_prompt']},
            *history,
            {"role": "user", "content": prompt},

        ],
        temperature=cfg["temperature"],
        max_tokens=cfg["maxOutputTokens"],
        top_p=cfg["top_p"],
        frequency_penalty=cfg["frequencyPenalty"],
        presence_penalty=cfg["presencePenalty"],
    )
    
    return response.choices[0].message.content