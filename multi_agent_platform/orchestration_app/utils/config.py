from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from pathlib import Path
import json

env_path = Path(__file__).resolve().parent.parent / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=str(env_path), env_file_encoding="utf-8")
    OPENAI_API_KEY: str
    LANGSMITH_TRACING: bool
    LANGSMITH_ENDPOINT: str
    LANGSMITH_API_KEY: str
    LANGSMITH_PROJECT: str
    ANTHROPIC_API_KEY: str
    GOOGLE_API_KEY: str
    TAVILY_API_KEY: str
    DB_URI: str
    CONNECTION_KWARGS: dict

    @field_validator("CONNECTION_KWARGS", mode="before")
    @classmethod
    def parse_json(cls, v):
        if isinstance(v, str):
            return json.loads(v)
        return v


settings = Settings()
