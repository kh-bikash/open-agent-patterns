from __future__ import annotations

import json
from pathlib import Path

from open_agent_patterns.engine import BenchmarkCase, PatternRegistry, SafeFallbackPattern


def main() -> None:
    cases = [BenchmarkCase(**row) for row in json.loads((Path(__file__).parent / "cases.json").read_text())]
    registry = PatternRegistry()
    registry.register(SafeFallbackPattern(lambda task: task.upper(), lambda task: "UNAVAILABLE"))
    result = registry.benchmark("safe-fallback", cases)
    print(json.dumps(result.__dict__, indent=2))


if __name__ == "__main__":
    main()
