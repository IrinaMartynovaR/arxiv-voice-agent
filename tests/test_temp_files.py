from app.utils.temp_files import remove_file, write_bytes_to_temp_file


def test_write_bytes_to_temp_file_closes_file() -> None:
    path = write_bytes_to_temp_file(b"audio", suffix=".wav")

    try:
        assert path.exists()
        assert path.read_bytes() == b"audio"
    finally:
        remove_file(path)


def test_remove_file_ignores_missing_file() -> None:
    path = write_bytes_to_temp_file(b"audio", suffix=".wav")
    remove_file(path)

    remove_file(path)

    assert not path.exists()
