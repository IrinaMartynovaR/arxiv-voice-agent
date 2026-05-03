from abc import ABC, abstractmethod


class AsrService(ABC):
    """Интерфейс сервиса распознавания речи."""

    @abstractmethod
    async def transcribe(self, audio_path: str) -> str:
        """Распознает речь из аудиофайла.

        Args:
            audio_path: Путь к аудиофайлу.

        Returns:
            Распознанный текст.
        """

