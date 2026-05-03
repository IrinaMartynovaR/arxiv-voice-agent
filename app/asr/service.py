from functools import lru_cache

from app.asr.base import AsrService
from app.asr.faster_whisper import FasterWhisperAsrService


@lru_cache
def get_asr_service() -> AsrService:
    """Возвращает singleton ASR-сервиса.

    Returns:
        Сервис распознавания речи.
    """
    return FasterWhisperAsrService()

