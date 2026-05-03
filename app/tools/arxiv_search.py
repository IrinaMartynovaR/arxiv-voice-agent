import asyncio
import logging

import arxiv
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class ArxivPaper(BaseModel):
    title: str
    summary: str
    authors: list[str] = Field(default_factory=list)
    published_year: int | None = None
    url: str
    pdf_url: str | None = None


async def search_arxiv(query: str, max_results: int = 5) -> list[ArxivPaper]:
    """Ищет статьи в arXiv.

    Args:
        query: Поисковый запрос.
        max_results: Максимальное количество результатов.

    Returns:
        Список нормализованных статей.
    """
    return await asyncio.to_thread(_search_arxiv_sync, query, max_results)


def _search_arxiv_sync(query: str, max_results: int) -> list[ArxivPaper]:
    """Синхронно выполняет запрос к arXiv.

    Args:
        query: Поисковый запрос.
        max_results: Максимальное количество результатов.

    Returns:
        Список нормализованных статей.
    """
    client = arxiv.Client()
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance,
    )

    papers: list[ArxivPaper] = []
    for result in client.results(search):
        papers.append(
            ArxivPaper(
                title=result.title,
                summary=result.summary,
                authors=[author.name for author in result.authors],
                published_year=result.published.year if result.published else None,
                url=result.entry_id,
                pdf_url=result.pdf_url,
            )
        )

    logger.info("arXiv papers fetched", extra={"query": query, "papers_count": len(papers)})
    return papers

