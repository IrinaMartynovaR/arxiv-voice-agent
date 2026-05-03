from functools import lru_cache

from app.agent.models import AgentResult
from app.graph.builder import build_research_graph


class AgentService:
    """Фасад для общения с LangGraph-агентом."""

    def __init__(self) -> None:
        self._graph = build_research_graph()

    async def ask(self, question: str) -> AgentResult:
        """Отправляет вопрос в граф агента.

        Args:
            question: Вопрос пользователя.

        Returns:
            Нормализованный ответ агента.
        """
        state = await self._graph.ainvoke({"question": question})
        return AgentResult(answer=state["answer"], papers=state.get("papers", []))


@lru_cache
def get_agent_service() -> AgentService:
    """Возвращает singleton сервиса агента.

    Returns:
        Сервис агента с собранным графом.
    """
    return AgentService()

