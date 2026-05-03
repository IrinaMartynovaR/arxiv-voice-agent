import logging

from app.settings.config import get_settings


def configure_logging() -> None:
    """Настраивает логирование приложения."""
    settings = get_settings()
    logging.basicConfig(
        level=settings.log_level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

