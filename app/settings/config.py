from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки приложения."""

    app_name: str = "arXiv Voice Agent"
    app_version: str = "0.1.0"
    log_level: str = "INFO"
    arxiv_max_results: int = 5
    asr_model_size: str = "base"
    asr_device: str = "cpu"

    model_config = SettingsConfigDict(env_file=".env", env_prefix="AVA_")


@lru_cache
def get_settings() -> Settings:
    """Возвращает настройки приложения.

    Returns:
        Настройки из переменных окружения и дефолтных значений.
    """
    return Settings()

