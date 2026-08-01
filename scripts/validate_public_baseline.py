#!/usr/bin/env python3
"""Validate the public CLARYEL Box Core baseline.

Проверить публичную основу CLARYEL Box Core.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = (
    "README.md",
    "AGENTS.md",
    "CLAUDE.md",
    "REPOSITORY.yaml",
    "NEXT_STEPS.md",
    "ARCHITECTURE.md",
    "OPEN_SOURCE_SCOPE.md",
    "PUBLICATION_STATUS.md",
    "GRANT_SCOPE.md",
    "BUDGET.md",
    "MILESTONES.md",
    "SECURITY.md",
    "THREAT_MODEL.md",
    "HARDWARE_COMPATIBILITY.md",
    "flake.nix",
    "schemas/desired-state.schema.json",
    "schemas/hardware-profile.schema.json",
)

# English: These patterns are intentionally conservative and are not a substitute for dedicated scanners.
# Русский: Эти шаблоны намеренно консервативны и не заменяют специализированные scanners.
FORBIDDEN_PATTERNS = {
    "private IPv4 address": re.compile(r"\b(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3}|172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3})\b"),
    "GitHub token": re.compile(r"\b(?:ghp|github_pat)_[A-Za-z0-9_]{20,}\b"),
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "Cloudflare token assignment": re.compile(r"(?i)\bCLOUDFLARE_(?:API_)?TOKEN\s*=\s*[^\s'\"]+"),
    "generic secret assignment": re.compile(r"(?i)\b(?:password|passwd|secret|api[_-]?key|token)\s*=\s*['\"][^'\"]{8,}['\"]"),
}

TEXT_SUFFIXES = {
    ".md",
    ".txt",
    ".yaml",
    ".yml",
    ".json",
    ".nix",
    ".rego",
    ".py",
    ".js",
    ".ts",
    ".sh",
}


def fail(message: str) -> None:
    """Record a fatal validation error.

    Зафиксировать критическую ошибку проверки.
    """

    print(f"ERROR: {message}", file=sys.stderr)


def validate_required_files() -> list[str]:
    """Check the repository governance baseline.

    Проверить обязательную основу управления репозиторием.
    """

    errors: list[str] = []
    for relative in REQUIRED_FILES:
        if not (ROOT / relative).is_file():
            errors.append(f"missing required file: {relative}")
    return errors


def validate_json_files() -> list[str]:
    """Parse every public JSON document.

    Разобрать каждый публичный JSON-документ.
    """

    errors: list[str] = []
    for path in sorted(ROOT.rglob("*.json")):
        if ".git" in path.parts:
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            errors.append(f"invalid JSON {path.relative_to(ROOT)}: {exc}")
    return errors


def validate_public_text() -> list[str]:
    """Scan public text for obvious forbidden material.

    Проверить публичный текст на очевидные запрещённые материалы.
    """

    errors: list[str] = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if ".git" in path.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"cannot read {path.relative_to(ROOT)}: {exc}")
            continue
        for label, pattern in FORBIDDEN_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"{label} detected in {path.relative_to(ROOT)}")
    return errors


def validate_status_language() -> list[str]:
    """Ensure the repository does not claim an unawarded grant.

    Убедиться, что репозиторий не заявляет о неприсуждённом гранте как о полученном.
    """

    errors: list[str] = []
    for path in sorted(ROOT.rglob("*.md")):
        text = path.read_text(encoding="utf-8").lower()
        forbidden_claims = (
            "ngi fediversity grant awarded",
            "ngi fediversity funded project",
            "грант ngi fediversity получен",
            "финансирование ngi fediversity присуждено",
        )
        for claim in forbidden_claims:
            if claim in text:
                errors.append(f"unverified award claim in {path.relative_to(ROOT)}: {claim}")
    return errors


def main() -> int:
    """Run all deterministic public-baseline checks.

    Выполнить все детерминированные проверки публичной основы.
    """

    errors = [
        *validate_required_files(),
        *validate_json_files(),
        *validate_public_text(),
        *validate_status_language(),
    ]
    if errors:
        for error in errors:
            fail(error)
        return 1

    print("CLARYEL Box Core public baseline validation passed.")
    print("Проверка публичной основы CLARYEL Box Core пройдена.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
