"""Central logging: JSON lines to stdout and a shared `mediatr` logger."""

from __future__ import annotations

import logging
import sys
from typing import Final

from pythonjsonlogger.json import JsonFormatter

LOGGER_NAME: Final = "mediatr"
_configured = False

logger = logging.getLogger(LOGGER_NAME)


def configure_logging(level: int = logging.INFO) -> None:
    """Idempotent setup; call once from the process entrypoint before other app imports."""
    global _configured
    if _configured:
        return

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        JsonFormatter(
            fmt="%(asctime)s %(name)s %(levelname)s %(module)s %(message)s",
            rename_fields={
                "levelname": "level",
                "name": "logger",
                "asctime": "timestamp",
            },
            json_ensure_ascii=False,
        )
    )

    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(level)
    _configured = True
