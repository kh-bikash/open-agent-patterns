import pytest

from open_agent_patterns.engine import (
    BenchmarkCase,
    PatternRegistry,
    SafeFallbackPattern,
)


def test_plugin_and_benchmark():
    registry = PatternRegistry()
    registry.register(
        SafeFallbackPattern(
            lambda _: (_ for _ in ()).throw(TimeoutError()), lambda task: task.upper()
        )
    )
    result = registry.benchmark(
        "safe-fallback", [BenchmarkCase("a", "A"), BenchmarkCase("b", "B")]
    )
    assert result.accuracy == 1 and result.cases == 2
    with pytest.raises(ValueError):
        registry.register(SafeFallbackPattern(lambda x: x, lambda x: x))
