import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    openai_api_key: str = ""
    default_model: str = "gpt-4o-mini"
    db_url: str = "sqlite:///./chat_sessions.db"
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()

# Прайсинг за токен для різних моделей
PRICING = {
    "gpt-4o-mini": {
        "prompt_price_per_token": 0.150 / 1000000,
        "completion_price_per_token": 0.600 / 1000000,
    },
    "gpt-4o": {
        "prompt_price_per_token": 2.50 / 1000000,
        "completion_price_per_token": 10.00 / 1000000,
    },
    "gpt-4": {
        "prompt_price_per_token": 30.00 / 1000000,
        "completion_price_per_token": 60.00 / 1000000,
    }
}
