from app.utils.files import get_suffix


def test_get_suffix_from_filename() -> None:
    assert get_suffix("question.webm") == ".webm"


def test_get_suffix_uses_default_for_missing_extension() -> None:
    assert get_suffix("question") == ".wav"


def test_get_suffix_uses_default_for_missing_filename() -> None:
    assert get_suffix(None) == ".wav"
