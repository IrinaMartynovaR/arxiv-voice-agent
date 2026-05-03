from pathlib import Path


def get_suffix(filename: str | None, default: str = ".wav") -> str:
    """Возвращает расширение файла.

    Args:
        filename: Имя файла.
        default: Расширение по умолчанию.

    Returns:
        Расширение файла или значение по умолчанию.
    """
    suffix = Path(filename or "").suffix
    return suffix or default

