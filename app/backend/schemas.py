from pydantic import BaseModel, Field, field_validator

from app.tools.arxiv_search import ArxivPaper


class HealthResponse(BaseModel):
    status: str


class ChatRequest(BaseModel):
    question: str = Field(min_length=1)

    @field_validator("question")
    @classmethod
    def normalize_question(cls, question: str) -> str:
        """Нормализует вопрос пользователя.

        Args:
            question: Вопрос пользователя.

        Returns:
            Вопрос без пробелов по краям.
        """
        normalized_question = question.strip()
        if not normalized_question:
            raise ValueError("question must not be blank")
        return normalized_question


class ChatResponse(BaseModel):
    answer: str
    papers: list[ArxivPaper] = Field(default_factory=list)


class VoiceResponse(ChatResponse):
    question: str
