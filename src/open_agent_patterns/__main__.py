"""Resilient text transformation through primary and fallback HTTP handlers."""

from __future__ import annotations

import argparse
import json
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from .engine import SafeFallbackPattern
from .web import serve

WEB_ACTIONS = {
    "run": [
        ("task", "Input text", "textarea", True),
        ("primary_url", "Primary HTTPS endpoint", "text", True),
        ("fallback_url", "Fallback HTTPS endpoint", "text", True),
    ]
}


def _endpoint(url: str, timeout: float):
    parsed = urlparse(url)
    if parsed.scheme != "https" and not (
        parsed.scheme == "http" and parsed.hostname in {"localhost", "127.0.0.1", "::1"}
    ):
        raise ValueError("endpoints require HTTPS or loopback")

    def call(task: str) -> str:
        request = Request(
            url,
            data=json.dumps({"task": task}).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urlopen(request, timeout=timeout) as response:
                data = json.load(response)
        except HTTPError as exc:
            if exc.code in {429, 500, 502, 503, 504}:
                raise RuntimeError("transient endpoint error") from exc
            raise
        except (URLError, TimeoutError) as exc:
            raise ConnectionError("endpoint unavailable") from exc
        if not isinstance(data, dict) or not isinstance(data.get("output"), str):
            raise TypeError("endpoint must return a JSON object with string output")
        return data["output"]

    return call


def execute(action: str, values: dict, *, timeout: float) -> object:
    if action != "run":
        raise ValueError("unknown action")
    if timeout <= 0:
        raise ValueError("timeout must be positive")
    pattern = SafeFallbackPattern(
        _endpoint(values["primary_url"], timeout),
        _endpoint(values["fallback_url"], timeout),
    )
    return {"output": pattern.run(values["task"], {}), "pattern": pattern.name}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Primary/fallback HTTP text handler")
    parser.add_argument("--timeout", type=float, default=10)
    commands = parser.add_subparsers(dest="command", required=True)
    run = commands.add_parser("run")
    run.add_argument("task")
    run.add_argument("--primary-url", required=True)
    run.add_argument("--fallback-url", required=True)
    browser = commands.add_parser("serve")
    browser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args(argv)
    if args.command == "serve":
        serve(
            "Open Agent Fallback Pattern",
            WEB_ACTIONS,
            lambda action, values: execute(action, values, timeout=args.timeout),
            port=args.port,
        )
    else:
        print(
            json.dumps(
                execute(args.command, vars(args), timeout=args.timeout), indent=2
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
