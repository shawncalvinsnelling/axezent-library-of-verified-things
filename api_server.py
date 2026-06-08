#!/usr/bin/env python3
"""No-dependency local API for the Axezent AI Library of Verified Things."""
from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse

from verify import verify_receipt

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"


class Handler(BaseHTTPRequestHandler):
    server_version = "AXZLVT/0.1"

    def _send_json(self, payload: dict, status: int = 200) -> None:
        raw = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(raw)

    def _send_file(self, path: Path) -> None:
        if not path.exists() or not path.is_file():
            self._send_json({"error": "not found"}, 404)
            return
        content_type = "text/html; charset=utf-8"
        if path.suffix == ".css":
            content_type = "text/css; charset=utf-8"
        elif path.suffix == ".js":
            content_type = "application/javascript; charset=utf-8"
        elif path.suffix == ".json":
            content_type = "application/json; charset=utf-8"
        raw = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/health":
            self._send_json({"status": "ok", "engine": "Axezent AI Library of Verified Things"})
        elif parsed.path == "/library":
            self._send_file(ROOT / "data" / "library.json")
        elif parsed.path in {"/", "/index.html"}:
            self._send_file(SITE / "index.html")
        elif parsed.path.startswith("/assets/"):
            self._send_file(SITE / parsed.path.lstrip("/"))
        elif parsed.path in {"/app.js", "/styles.css"}:
            self._send_file(SITE / parsed.path.lstrip("/"))
        else:
            self._send_json({"error": "not found"}, 404)

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path != "/verify":
            self._send_json({"error": "not found"}, 404)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            data = json.loads(self.rfile.read(length).decode("utf-8"))
            if not isinstance(data, dict):
                raise ValueError("receipt must be a JSON object")
            report = verify_receipt(data)
            self._send_json(report.to_dict(), 200)
        except Exception as exc:
            self._send_json({"result": "ERROR", "errors": [str(exc)]}, 400)


def main() -> int:
    host = "127.0.0.1"
    port = 8000
    print(f"Axezent AI Library of Verified Things running at http://{host}:{port}")
    print("POST receipts to http://127.0.0.1:8000/verify")
    HTTPServer((host, port), Handler).serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
