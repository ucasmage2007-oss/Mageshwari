from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "EduGenie"
    host: str = "127.0.0.1"
    port: int = 8000
    reload: bool = True

    gemini_api_key: str = ""
    gemini_model: str = "gemini-3.8-flash"

    # The project specification calls for LaMini-Flan-T5-783M for concept explanation.
    # Keep it optional because the local model is large and can be CPU-intensive.

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
