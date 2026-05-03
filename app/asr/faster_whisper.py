import asyncio
import logging

from app.asr.base import AsrService
from app.settings.config import get_settings
from app.utils.errors import ServiceUnavailableError

logger = logging.getLogger(__name__)


class FasterWhisperAsrService(AsrService):
    """ASR-сервис на базе faster-whisper."""

    def __init__(self) -> None:
        settings = get_settings()
        try:
            from faster_whisper import WhisperModel
        except ImportError as exc:
            message = 'Установи ASR-зависимости командой: uv sync --extra asr'
            raise ServiceUnavailableError(message) from exc

        self._model = WhisperModel(settings.asr_model_size, device=settings.asr_device)

    async def transcribe(self, audio_path: str) -> str:
        """Распознает речь из аудиофайла.

        Args:
            audio_path: Путь к аудиофайлу.

        Returns:
            Распознанный текст.
        """
        return await asyncio.to_thread(self._transcribe_sync, audio_path)

    def _transcribe_sync(self, audio_path: str) -> str:
        """Синхронно распознает аудио через faster-whisper.

        Args:
            audio_path: Путь к аудиофайлу.

        Returns:
            Распознанный текст.
        """
        segments, _info = self._model.transcribe(audio_path, beam_size=5)
        text = " ".join(segment.text.strip() for segment in segments).strip()
        logger.info("Audio transcribed", extra={"audio_path": audio_path, "text_length": len(text)})
        return text

