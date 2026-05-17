import logging
from pathlib import Path
from tempfile import NamedTemporaryFile

logger = logging.getLogger(__name__)


def write_bytes_to_temp_file(content: bytes, suffix: str) -> Path:
    """Сохраняет байты во временный файл.

    Args:
        content: Содержимое файла.
        suffix: Расширение временного файла.

    Returns:
        Путь к закрытому временному файлу.
    """
    with NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        temp_file.write(content)
        return Path(temp_file.name)


def remove_file(path: Path) -> None:
    """Удаляет файл, если он существует.

    Args:
        path: Путь к файлу.
    """
    try:
        path.unlink(missing_ok=True)
    except OSError:
        logger.exception("Failed to remove temporary file", extra={"path": str(path)})
