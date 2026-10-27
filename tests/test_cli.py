import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from open_agent_patterns.__main__ import execute


def test_product_uses_fallback_endpoint_after_transient_failure():
    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):
            length = int(self.headers["Content-Length"])
            task = json.loads(self.rfile.read(length))["task"]
            if self.path == "/primary":
                self.send_response(503)
                self.end_headers()
                return
            body = json.dumps({"output": task.upper()}).encode()
            self.send_response(200)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    server = HTTPServer(("127.0.0.1", 0), Handler)
    worker = threading.Thread(target=server.serve_forever, daemon=True)
    worker.start()
    try:
        base = f"http://127.0.0.1:{server.server_port}"
        result = execute(
            "run",
            {
                "task": "hello",
                "primary_url": base + "/primary",
                "fallback_url": base + "/backup",
            },
            timeout=2,
        )
        assert result["output"] == "HELLO"
    finally:
        server.shutdown()
        server.server_close()
        worker.join()
