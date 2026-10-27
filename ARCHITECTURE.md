# Architecture

## Goal

Define a small agent pattern interface, register extensions, and benchmark a safe fallback pattern.

## Request path

Pattern protocol -> registration with unique name -> context-isolated invocation -> benchmark cases -> accuracy and latency report.

## Components

- `src/open_agent_patterns/engine.py`: policy and state transitions for this project.
- `src/open_agent_patterns/langgraph_adapter.py`: optional StateGraph integration with a fallback branch.

- `tests/test_engine.py`: deterministic behavior and failure tests.
- `.github/workflows/ci.yml`: install and test gate.


## State and failure behavior

This repository is a standalone reference extension and contribution package. It does not claim an upstream LangGraph, CrewAI, or AutoGen merge. Choose an upstream project, adapt its interface and tests, and submit a PR under that project's contribution rules.

The application should propagate failed operations to its caller or queue so the caller can decide whether to retry. Input and handler output are treated as untrusted at the integration boundary.

## Operations checklist

1. Set secrets through a secret manager and rotate them regularly.
2. Put the service or integrating application behind TLS and authentication.
3. This package is stateless; version benchmark datasets with code and keep handler secrets in the integrating application.
4. Run `pytest -q` in CI before deployment.
5. Define workload specific evaluation cases, latency objectives, and rollback criteria before serving real users.

## Extension and benchmark contract

`PatternRegistry` accepts objects implementing `name` and `run(task, context)` and rejects duplicate names. `SafeFallbackPattern` catches only transient timeout, connection, and runtime failures from its primary function. The optional `langgraph_adapter.py` builds a `StateGraph` with primary and fallback nodes. The graph takes one recovery branch and terminates; validation and programming errors still surface.

`benchmarks/cases.json` tests direct output accuracy. `benchmarks/failures.json` injects primary failures and compares baseline with recovery graph accuracy on the same cases. These deterministic cases prove branch behavior, not model quality or real provider savings. [TUTORIAL.md](TUTORIAL.md) shows installation and use. An upstream LangGraph PR needs a maintainer approved, assigned issue under its current contribution rules; this standalone package makes no claim of upstream acceptance.
