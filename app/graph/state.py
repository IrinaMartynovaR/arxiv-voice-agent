from typing import TypedDict

from app.tools.arxiv_search import ArxivPaper


class ResearchState(TypedDict, total=False):
    question: str
    answer: str
    papers: list[ArxivPaper]

