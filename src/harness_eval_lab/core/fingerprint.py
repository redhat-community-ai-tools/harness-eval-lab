"""Setup fingerprinting for change detection and deduplication."""

from __future__ import annotations

import hashlib
from pathlib import Path

RELEVANT_PATTERNS = [
    "CLAUDE.md",
    "**/CLAUDE.md",
    "skills/**/*.md",
    "commands/**/*.md",
    ".claude/settings.json",
    ".claude/settings.local.json",
    ".claude/agents/**/*.md",
    ".mcp.json",
    "**/.mcp.json",
]


def fingerprint_setup(setup_path: str) -> str:
    """Compute a stable SHA256 of all agent-relevant files in a setup directory."""
    root = Path(setup_path)
    if not root.is_dir():
        raise FileNotFoundError(f"Setup path does not exist: {setup_path}")

    file_hashes: list[tuple[str, str]] = []

    for pattern in RELEVANT_PATTERNS:
        for filepath in sorted(root.glob(pattern)):
            if filepath.is_file():
                rel = str(filepath.relative_to(root))
                content_hash = hashlib.sha256(filepath.read_bytes()).hexdigest()
                file_hashes.append((rel, content_hash))

    file_hashes.sort(key=lambda x: x[0])

    combined = hashlib.sha256()
    for rel_path, content_hash in file_hashes:
        combined.update(f"{rel_path}:{content_hash}\n".encode())

    return combined.hexdigest()


def fingerprints_match(a: str, b: str) -> bool:
    return a == b
