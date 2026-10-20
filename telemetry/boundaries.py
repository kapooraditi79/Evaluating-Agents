"""Shop evidence must stay separate from agent run records and evaluator data."""

from pathlib import Path

RESERVED_STORES = frozenset({"runs", "private"})


def in_reserved_store(path: Path) -> bool:
    """Directory-name checks are case-insensitive, including on non-Windows hosts."""
    return any(part.casefold() in RESERVED_STORES for part in path.absolute().parts)
