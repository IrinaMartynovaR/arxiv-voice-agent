from pydantic import BaseModel, Field

from app.tools.arxiv_search import ArxivPaper


class HealthResponse(BaseModel):
    status: str


class ChatRequest(BaseModel):
    question: str = Field(min_length=1)


class ChatResponse(BaseModel):
    answer: str
    papers: list[ArxivPaper] = Field(default_factory=list)


class VoiceResponse(ChatResponse):
    question: str

