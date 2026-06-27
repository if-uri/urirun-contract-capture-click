# WYGENEROWANE Z contracts.json — NIE EDYTUJ RĘCZNIE.
# Przegeneruj: `make gen`. Bramą jest ci/regen_check.py.
from typing import Any

# from .conn import conn, _ok  # zapewnione przez pakiet connectora

@conn.handler("abs/command/click", isolated=True, meta={"label": "TODO: abs/command/click"})
def click(x: int = 0, y: int = 0, sw: int = 0, sh: int = 0, button: str = "") -> dict[str, Any]:
    """WYGENEROWANE Z KONTRAKTU v1. Sygnatura i kształt koperty pochodzą z
    contracts.json — NIE edytuj ich ręcznie (build odrzuci dryf). Uzupełnij tylko ciało."""
    raise NotImplementedError("ciało abs/command/click")  # noqa: F841 — uzupełnij logikę, potem:
    return _ok(action='click-abs', screen=[], did="")

@conn.handler("screen/query/capture", isolated=True, meta={"label": "TODO: screen/query/capture"})
def capture(monitor: int = 0, max_width: int = 0, base64: bool = False) -> dict[str, Any]:
    """WYGENEROWANE Z KONTRAKTU v1. Sygnatura i kształt koperty pochodzą z
    contracts.json — NIE edytuj ich ręcznie (build odrzuci dryf). Uzupełnij tylko ciało."""
    raise NotImplementedError("ciało screen/query/capture")  # noqa: F841 — uzupełnij logikę, potem:
    return _ok(kind='screenshot', path="", bytes=0, fullSize=[], via="")  # oneOf — wariant Degraded zwróć osobną gałęzią
