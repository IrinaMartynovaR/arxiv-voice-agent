import logging

from app.graph.state import ResearchState
from app.settings.config import get_settings
from app.tools.arxiv_search import search_arxiv

logger = logging.getLogger(__name__)


async def search_papers_node(state: ResearchState) -> ResearchState:
    """Ищет статьи на arXiv по вопросу пользователя.

    Args:
        state: Текущее состояние графа.

    Returns:
        Состояние со списком найденных статей.
    """
    settings = get_settings()
    question = state["question"]
    papers = await search_arxiv(question, max_results=settings.arxiv_max_results)
    logger.info("arXiv search completed", extra={"papers_count": len(papers)})
    return {**state, "papers": papers}


async def compose_answer_node(state: ResearchState) -> ResearchState:
    """Формирует базовый ответ на основе найденных статей.

    Args:
        state: Текущее состояние графа.

    Returns:
        Состояние с текстовым ответом.
    """
    papers = state.get("papers", [])
    if not papers:
        return {**state, "answer": "Я не нашла подходящих статей на arXiv по этому запросу."}

    lines = ["Нашла несколько релевантных статей на arXiv:"]
    for index, paper in enumerate(papers, start=1):
        lines.append(f"{index}. {paper.title} ({paper.published_year}) - {paper.url}")

    return {**state, "answer": "\n".join(lines)}

