#!/usr/bin/env python3
# Part of the ifURI solution — pakiet PRODUCENTA (proces 1).
"""Serwis HTTP udostępniający ``screen/query/capture``. Zwraca kopertę zrzutu (Sukces lub
Degraded — oneOf), walidowaną wobec out-schematu wspólnego kontraktu PRZED wysłaniem. Pole
``fullSize`` (lista [int]) zasila potem przestrzeń kliknięcia konsumenta.

  POST /run  {monitor?, base64?}  →  koperta screen/query/capture
  GET  /health                    →  {"ok": true}
"""
from __future__ import annotations

import json
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "toolkit"))
from contract_gate import check  # noqa: E402
from contracts_io import load  # noqa: E402

ROUTE = "screen/query/capture"
CONTRACTS, _ = load()
C = CONTRACTS[ROUTE]


def capture_handler(monitor: int = 0, base64: bool = False) -> dict:
    # demo: a healthy frame (the degraded oneOf variant is returned when a portal placeholder is seen)
    return {"ok": True, "connector": "capture-click", "kind": "screenshot",
            "path": "/tmp/s.png", "bytes": 204931, "fullSize": [2560, 1440], "via": "grim"}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"ok": true}')

    def do_POST(self):
        body = self.rfile.read(int(self.headers.get("Content-Length", 0) or 0))
        payload = json.loads(body or b"{}")
        env = capture_handler(monitor=payload.get("monitor", 0), base64=payload.get("base64", False))
        try:
            check(C.out, env, "out")
        except AssertionError as exc:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"ok": False, "error": f"output violates {ROUTE}: {exc}"}).encode())
            return
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(env).encode())


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8801"))
    print(f"producer: {ROUTE} na :{port}", flush=True)
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()
