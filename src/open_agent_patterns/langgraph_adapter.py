from __future__ import annotations

from typing import Callable, NotRequired, TypedDict

from langgraph.graph import END, START, StateGraph


class FallbackState(TypedDict):
    task: str
    answer: NotRequired[str]
    error: NotRequired[str]


def build_fallback_graph(primary: Callable[[str], str], fallback: Callable[[str], str]):
    """Build an executable LangGraph with a recovery branch for transient failures."""

    def call_primary(state: FallbackState) -> dict[str, str]:
        try:
            return {"answer": primary(state["task"]), "error": ""}
        except (TimeoutError, ConnectionError, RuntimeError) as exc:
            return {"error": type(exc).__name__}

    def call_fallback(state: FallbackState) -> dict[str, str]:
        return {"answer": fallback(state["task"])}

    graph = StateGraph(FallbackState)
    graph.add_node("primary", call_primary)
    graph.add_node("fallback", call_fallback)
    graph.add_edge(START, "primary")
    graph.add_conditional_edges("primary", lambda state: "fallback" if state.get("error") else END)
    graph.add_edge("fallback", END)
    return graph.compile()
