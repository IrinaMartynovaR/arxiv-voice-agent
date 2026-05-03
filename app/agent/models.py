from pydantic import BaseModel, Field

from app.tools.arxiv_search import ArxivPaper


class AgentResult(BaseModel):
    answer: str
    papers: list[ArxivPaper] = Field(default_factory=list)

