from __future__ import annotations

import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any


def to_json_bytes(data: dict[Any, Any]) -> bytes:
    return json.dumps(data, separators=(",", ":")).encode("utf-8")
