# Contributing a pattern upstream

1. Read the current [LangGraph contribution guide](https://docs.langchain.com/oss/python/contributing/overview) and open a proposal issue or discussion. Its current pull request template requires a maintainer approved issue and assignment before an external PR.
2. Use `langgraph_adapter.py` as the starting integration. Preserve the bounded fallback behavior.
3. Add framework native unit tests for success, timeout, and fallback failure.
4. Run the benchmark dataset in `benchmarks/cases.json` against the old and new integration. Report accuracy, latency, environment, and model versions; do not claim an improvement without a measured baseline.
5. Add a small runnable example and architecture explanation to the upstream docs.
6. Open an upstream pull request and link the benchmark report and tests.

This repository has not submitted or merged an upstream pull request. It provides the reusable implementation and materials for one once the upstream prerequisites are met.
