from __future__ import annotations

import json
from pathlib import Path

from open_agent_patterns.engine import BenchmarkCase, PatternRegistry, SafeFallbackPattern
from open_agent_patterns.langgraph_adapter import build_fallback_graph


def main() -> None:
    cases = [BenchmarkCase(**row) for row in json.loads((Path(__file__).parent / "cases.json").read_text())]
    registry = PatternRegistry()
    registry.register(SafeFallbackPattern(lambda task: task.upper(), lambda task: "UNAVAILABLE"))
    result = registry.benchmark("safe-fallback", cases)
    failures = json.loads((Path(__file__).parent / "failures.json").read_text())
    fail_tasks = {row["task"] for row in failures if row["primary_fails"]}
    def primary(task):
        if task in fail_tasks:
            raise TimeoutError("injected transient failure")
        return task.upper()
    baseline_correct = 0
    for row in failures:
        try:
            baseline_correct += primary(row["task"]) == row["expected"]
        except TimeoutError:
            pass
    graph = build_fallback_graph(primary, lambda task: task.upper())
    graph_correct = sum(graph.invoke({"task": row["task"]})["answer"] == row["expected"] for row in failures)
    print(json.dumps({"pattern": result.__dict__, "failure_injection": {
        "cases": len(failures), "baseline_accuracy": baseline_correct / len(failures),
        "fallback_graph_accuracy": graph_correct / len(failures), "injected_failure_rate": len(fail_tasks) / len(failures)
    }}, indent=2))


if __name__ == "__main__":
    main()
