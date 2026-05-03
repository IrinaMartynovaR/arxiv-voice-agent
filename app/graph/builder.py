from typing import Any

from langgraph.graph import END, StateGraph
from langgraph.graph.state import CompiledStateGraph

from app.graph.nodes import compose_answer_node, search_papers_node
from app.graph.state import ResearchState


def build_research_graph() -> CompiledStateGraph[ResearchState, Any, Any, ResearchState]:
    """Собирает LangGraph-граф исследовательского агента.

    Returns:
        Скомпилированный graph runnable.
    """
    graph = StateGraph(ResearchState)
    graph.add_node("search_papers", search_papers_node)
    graph.add_node("compose_answer", compose_answer_node)

    graph.set_entry_point("search_papers")
    graph.add_edge("search_papers", "compose_answer")
    graph.add_edge("compose_answer", END)

    return graph.compile()
