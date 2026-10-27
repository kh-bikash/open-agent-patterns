# Build a LangGraph fallback pattern

This tutorial uses deterministic functions so it runs without a model account.

## Install and verify

```bash
python -m pip install -e '.[dev]'
pytest -q
python benchmarks/run.py
```

## Assemble the graph

```python
from open_agent_patterns.langgraph_adapter import build_fallback_graph

def primary(task: str) -> str:
    raise TimeoutError("primary provider unavailable")

def fallback(task: str) -> str:
    return f"Fallback handled: {task}"

graph = build_fallback_graph(primary, fallback)
print(graph.invoke({"task": "summarize the incident"}))
```

`primary` catches only transient failures. Validation and programming errors propagate so they are not hidden. The graph state records the error class and the final answer. The fallback node runs once, then the graph terminates. Set timeouts and retry policy in the provider adapters; this pattern limits the graph route, not provider latency.

## Benchmark and interpretation

`benchmarks/failures.json` marks which deterministic primary calls fail. `benchmarks/run.py` reports the baseline success rate and the graph's success rate on the same cases. This is a failure-injection check, not an LLM quality benchmark. To measure a real provider, replace the functions and cases with a representative held-out dataset, record provider versions and costs, and repeat runs to capture variance.

## Upstream contribution

Read [CONTRIBUTING.md](CONTRIBUTING.md). LangGraph currently requires a maintainer-approved, assigned issue before an external pull request. The adapter here is ready for review in this repository; it is not an upstream merge.
