import pytest
from pydantic import ValidationError

from app.backend.schemas import ChatRequest


def test_chat_request_strips_question() -> None:
    request = ChatRequest(question="  transformers in medicine  ")

    assert request.question == "transformers in medicine"


def test_chat_request_rejects_blank_question() -> None:
    with pytest.raises(ValidationError):
        ChatRequest(question="   ")
