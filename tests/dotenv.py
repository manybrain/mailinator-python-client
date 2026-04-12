from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable, Optional


def _parse_bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def load_dotenv(
    paths: Optional[Iterable[Path]] = None, *, override: bool = False
) -> Optional[Path]:
    """
    Minimal .env loader so integration tests can be configured without extra deps.

    - Loads the first existing file from `paths`.
    - Supports `KEY=VALUE` lines, optional quotes, and `export KEY=VALUE`.
    - Ignores blank lines and comments.
    """

    if paths is None:
        repo_root = Path(__file__).resolve().parents[1]
        paths = [
            repo_root / ".env",
            repo_root / ".env.local",
            repo_root / ".env.test",
            repo_root / "tests" / ".env",
            repo_root / "tests" / ".env.local",
        ]

    chosen: Optional[Path] = None
    for path in paths:
        if path.exists() and path.is_file():
            chosen = path
            break

    if chosen is None:
        return None

    for raw_line in chosen.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        if line.startswith("export "):
            line = line[len("export ") :].lstrip()

        if "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()

        if not key:
            continue

        if (
            (value.startswith('"') and value.endswith('"'))
            or (value.startswith("'") and value.endswith("'"))
        ) and len(value) >= 2:
            value = value[1:-1]

        if not override and key in os.environ:
            continue

        os.environ[key] = value

    return chosen


def env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None or value == "":
        return default
    return _parse_bool(value)


def env_int(name: str, default: int = 0) -> int:
    value = os.getenv(name)
    if value is None or value == "":
        return default
    try:
        return int(value)
    except ValueError:
        return default
