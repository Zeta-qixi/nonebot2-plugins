from pydantic import BaseModel, Field
from pathlib import Path
import os
from nonebot import get_driver, require, get_plugin_config

require("nonebot_plugin_localstore")
import nonebot_plugin_localstore as store

class Config(BaseModel):
    
    db_path: Path  = Field(default=store.get_plugin_data_file("llm_manager.db"))
    # 增加加密密钥配置，确保 .env 中有 LLM_TOKEN_ENCRYPT_KEY
    llm_token_encrypt_key: str = "pT8ZDjwCvnWkfPEYBm12q2p9srNkM-nWC6Ss9aAcMEw=" 

    class Config:
        extra = "ignore"

plugin_config = get_plugin_config(Config)