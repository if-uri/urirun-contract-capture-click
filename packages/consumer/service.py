#!/usr/bin/env python3
# Part of the ifURI solution — pakiet KONSUMENTA (proces 2).
"""Serwis HTTP udostępniający ``abs/command/click``. Klika piksel (x,y) w przestrzeni ekranu
(sw,sh). WALIDUJE wejście wobec inp-schematu wspólnego kontraktu — x,y są WYMAGANE, sw,sh
opcjonalne (przychodzą z krawędzi WIRES od zrzutu; x,y z osobnego kroku locate). Ładuje TEN SAM
contracts.json co producent.

  POST /run  {x, y, sw?, sh?, button?}  →  koperta abs/command/click
  GET  /health                          →  {"ok": true}
"""
from __future__ import annotations

import json
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "toolkit"))
from contract_gate import check  # noqa: E402
from contracts_io import load  # noqa: E402

ROUTE = "abs/command/click"
CONTRACTS, _ = load()
C = CONTRACTS[ROUTE]


def click_handler(x: int, y: int, sw: int = 0, sh: int = 0, button: str = "left") -> dict:
    return {"ok": True, "connector": "capture-click", "action": "click-abs",
            "screen": [sw, sh], "did": f"click@({x},{y})"}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _err(self, code, msg):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"ok": False, "error": msg}).encode())

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"ok": true}')

    def do_POST(self):
        body = self.rfile.read(int(self.headers.get("Content-Length", 0) or 0))
        payload = json.loads(body or b"{}")
        try:
            check(C.inp, payload, "inp")
        except AssertionError as exc:
            return self._err(422, f"input violates {ROUTE}: {exc}")
        env = click_handler(x=payload["x"], y=payload["y"], sw=payload.get("sw", 0),
                            sh=payload.get("sh", 0), button=payload.get("button", "left"))
        try:
            check(C.out, env, "out")
        except AssertionError as exc:
            return self._err(500, f"output violates {ROUTE}: {exc}")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(env).encode())


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8802"))
    print(f"consumer: {ROUTE} na :{port}", flush=True)
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()
