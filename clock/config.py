from pydantic import BaseModel, Field
from pathlib import Path
from nonebot import require, get_plugin_config

require("nonebot_plugin_localstore")
import nonebot_plugin_localstore as store

class Config(BaseModel):
    db_path: Path  = Field(default=store.get_plugin_data_file("data.db"))
    group_at_me: bool = Field(default=True)
    use_llm: bool = Field(default=True)

clock_config = get_plugin_config(Config)

DB_PATH = clock_config.db_path
IMAGE_DIR = store.get_plugin_data_file('images')
USE_LLM = clock_config.use_llm