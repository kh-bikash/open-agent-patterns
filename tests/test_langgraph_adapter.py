from open_agent_patterns.langgraph_adapter import build_fallback_graph


def test_langgraph_success():
    graph = build_fallback_graph(lambda task: task.upper(), lambda _: "fallback")
    assert graph.invoke({"task": "hello"})["answer"] == "HELLO"


def test_langgraph_recovers_transient_failure():
    def fail(_):
        raise TimeoutError("timed out")
    graph = build_fallback_graph(fail, lambda task: "recovered " + task)
    result = graph.invoke({"task": "hello"})
    assert result["answer"] == "recovered hello"
    assert result["error"] == "TimeoutError"
