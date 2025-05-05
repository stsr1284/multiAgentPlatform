from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    OPENAI_API_KEY: str
    # LANGCHAIN_TRACING_V2: bool
    # LANGCHAIN_ENDPOINT: str
    # LANGCHAIN_API_KEY: str


settings = Settings()
