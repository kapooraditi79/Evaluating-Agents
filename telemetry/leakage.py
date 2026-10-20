"""Audit public values, attributes, paths and Parquet metadata. Never open private files."""

import json
import re
from collections.abc import Mapping
from pathlib import Path

import pyarrow.parquet as pq

from telemetry.boundaries import in_reserved_store

FORBIDDEN = re.compile(
    r"(?i)(?<![a-z])(injected|fault|chaos|decoy|scenario|archetype|seed|ground[ _-]truth)(?![a-z])"
)


def audit_public(root: Path, allowed_adversarial_bodies: frozenset[str] = frozenset()) -> list[str]:
    failures: list[str] = []

    def contains(value: object) -> bool:
        if isinstance(value, bytes):
            value = value.decode("utf-8", errors="replace")
        if isinstance(value, str):
            return bool(FORBIDDEN.search(value))
        if isinstance(value, Mapping):
            return any(contains(k) or contains(v) for k, v in value.items())
        if isinstance(value, (list, tuple)):
            return any(contains(item) for item in value)
        return False

    def linked(path: Path) -> bool:
        return path.is_symlink() or path.is_junction()

    def files(directory: Path):
        for child in sorted(directory.iterdir()):
            if in_reserved_store(child):
                failures.append(f"store boundary: {child.name}")
            elif linked(child):
                failures.append(f"symlink: {child.name}")
            elif child.is_dir():
                yield from files(child)
            elif child.is_file():
                yield child

    def field_metadata(field) -> bool:
        if contains(field.metadata or {}):
            return True
        return any(
            field_metadata(field.type.field(i)) for i in range(getattr(field.type, "num_fields", 0))
        )

    if in_reserved_store(root):
        return ["store boundary: root is inside runs/ or private/"]
    if linked(root) or any(linked(parent) for parent in root.parents):
        return ["symlink: public root"]
    for path in files(root):
        if FORBIDDEN.search(path.relative_to(root).as_posix()):
            failures.append(f"name: {path.name}")
        if path.suffix.lower() == ".parquet":
            table = pq.read_table(path)
            # ARROW:schema is base64 binary; its decoded field metadata is checked below.
            metadata = {
                k: v
                for k, v in (pq.read_metadata(path).metadata or {}).items()
                if k != b"ARROW:schema"
            }
            if (
                contains(metadata)
                or contains(pq.read_metadata(path).created_by)
                or any(field_metadata(field) for field in table.schema)
            ):
                failures.append(f"metadata: {path.name}")
            for i, row in enumerate(table.to_pylist()):
                # Only the exact allowlisted log BODY is exempt; attributes are always audited.
                if path.name == "logs.parquet" and row.get("body") in allowed_adversarial_bodies:
                    row = {k: v for k, v in row.items() if k != "body"}
                if isinstance(row.get("attributes"), str):
                    try:
                        row["attributes"] = json.loads(row["attributes"])
                    except json.JSONDecodeError:
                        failures.append(f"invalid attributes: {path.name}:{i}")
                if contains(row):
                    failures.append(f"content: {path.name}:{i}")
        else:
            try:
                text = path.read_text(encoding="utf-8")
                value = json.loads(text) if path.suffix.lower() == ".json" else text
                if contains(value):
                    failures.append(f"content: {path.name}")
            except (UnicodeError, json.JSONDecodeError):
                failures.append(f"unreadable public text: {path.name}")
    return failures
