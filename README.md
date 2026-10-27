# Open Agent Patterns

Define a small agent pattern interface, register extensions, and benchmark a safe fallback pattern.

## Quick start

Requires Python 3.11 or newer. From this repository:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e '.[dev]'
pytest -q
```

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
pytest -q
```

This project uses deterministic tests and needs no model key for verification.

```python
from open_agent_patterns.engine import BenchmarkCase, PatternRegistry, SafeFallbackPattern

registry = PatternRegistry()
registry.register(SafeFallbackPattern(lambda task: task.upper(), lambda task: "unavailable"))
print(registry.benchmark("safe-fallback", [BenchmarkCase("hello", "HELLO")]))
```

## Architecture

Pattern protocol -> registration with unique name -> context-isolated invocation -> benchmark cases -> accuracy and latency report.

See [ARCHITECTURE.md](ARCHITECTURE.md) for components, state, failure behavior, and operations.

## Deployment and safety

This repository is a standalone reference extension and contribution package. It does not claim an upstream LangGraph, CrewAI, or AutoGen merge. Choose an upstream project, adapt its interface and tests, and submit a PR under that project's contribution rules.

The optional LangGraph adapter in `src/open_agent_patterns/langgraph_adapter.py` builds a runnable recovery graph. Install `.[langgraph]` to use it. `python benchmarks/run.py` runs the deterministic benchmark dataset; see [CONTRIBUTING.md](CONTRIBUTING.md) before proposing an upstream PR.

See [TUTORIAL.md](TUTORIAL.md) for a complete LangGraph walkthrough and the limits of the failure-injection benchmark.

Install this as a library in an authenticated application or worker. Register trusted handlers and keep application secrets outside source control.

## Verification

`pytest -q` runs deterministic tests. GitHub Actions runs the same suite on pushes and pull requests.

## License

MIT. See [LICENSE](LICENSE).
