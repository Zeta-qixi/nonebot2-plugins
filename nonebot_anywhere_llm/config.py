class PluginConfig:
    openai_api_key: str = ""
    openai_base_url: str = "https://api.openai.com/v1"
    default_model: str = "gpt-3.5-turbo"
    max_history_length: int = 10
    enable_db_history: bool = True

    class Config:
        extra = "ignore"