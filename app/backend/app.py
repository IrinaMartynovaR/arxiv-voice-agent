from fastapi import FastAPI

from app.backend.routes import router
from app.settings.config import get_settings
from app.settings.logging import configure_logging


def create_app() -> FastAPI:
    """Создает FastAPI-приложение.

    Returns:
        Сконфигурированный экземпляр FastAPI.
    """
    configure_logging()
    settings = get_settings()

    application = FastAPI(title=settings.app_name, version=settings.app_version)
    application.include_router(router)
    return application

