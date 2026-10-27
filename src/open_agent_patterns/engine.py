from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any, Callable, Protocol


class Pattern(Protocol):
    name: str
    def run(self, task: str, context: dict[str, Any]) -> str: ...


@dataclass(frozen=True)
class BenchmarkCase:
    task: str
    expected: str


@dataclass(frozen=True)
class BenchmarkResult:
    pattern: str
    accuracy: float
    mean_latency_ms: float
    cases: int


class PatternRegistry:
    def __init__(self):
        self._patterns: dict[str, Pattern] = {}

    def register(self, pattern: Pattern) -> None:
        if not pattern.name or pattern.name in self._patterns:
            raise ValueError("pattern name empty or already registered")
        self._patterns[pattern.name] = pattern

    def run(self, name: str, task: str, context: dict[str, Any] | None = None) -> str:
        return self._patterns[name].run(task, dict(context or {}))

    def benchmark(self, name: str, cases: list[BenchmarkCase], *, scorer: Callable[[str, str], bool] | None = None) -> BenchmarkResult:
        if not cases:
            raise ValueError("benchmark needs at least one case")
        scorer = scorer or (lambda actual, expected: actual.strip() == expected.strip())
        correct = 0
        started = time.monotonic()
        for case in cases:
            actual = self.run(name, case.task)
            correct += bool(scorer(actual, case.expected))
        return BenchmarkResult(name, correct / len(cases), (time.monotonic() - started) * 1000 / len(cases), len(cases))


@dataclass(frozen=True)
class SafeFallbackPattern:
    """Example extension: recover from a primary agent failure with a fallback."""

    primary: Callable[[str], str]
    fallback: Callable[[str], str]
    name: str = "safe-fallback"

    def run(self, task: str, context: dict[str, Any]) -> str:
        try:
            return self.primary(task)
        except (TimeoutError, ConnectionError, RuntimeError):
            return self.fallback(task)
