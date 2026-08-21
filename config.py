import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    openai_api_key: str = ""
    model_name: str = "gpt-4o-mini"
    db_url: str = "sqlite:///./chat_sessions.db"
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()

PRICING = {
    "gpt-4o-mini": {
        "prompt_price_per_token": 0.150 / 1000000,
        "completion_price_per_token": 0.600 / 1000000,
    }
}
