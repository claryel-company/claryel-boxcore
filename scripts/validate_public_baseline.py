#!/usr/bin/env python3
"""Validate the public CLARYEL Box Core baseline without private services."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

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
    "CONTRIBUTING.md",
    "LICENSE",
    "LICENSES/README.md",
    "flake.nix",
    "schemas/desired-state.schema.json",
    "schemas/hardware-profile.schema.json",
    "schemas/change-plan.schema.json",
    "examples/systems/home.json",
    "examples/change-plan-low-risk.json",
    "examples/change-plan-high-risk.json",
    "policy/risk-policy.rego",
    "policy/risk-policy_test.rego",
    "docs/LANGUAGE_POLICY.md",
    "docs/STATUS_MODEL.md",
    "docs/COMPETITIVE_LANDSCAPE.md",
    "docs/GRANT_ALIGNMENT.md",
    "docs/DEMO_AND_EVIDENCE_PLAN.md",
    "docs/QUICKSTART.md",
    "docs/FAQ.md",
    "docs/PRIVATE_EXPORT_INVENTORY.md",
    "docs/PROVENANCE.md",
    "site-content/project.json",
    "site-content/status.json",
    "site-content/grant.json",
)

IMPLEMENTATION_STATUSES = {
    "planned",
    "experimental",
    "validated",
    "production-ready",
    "private-testing",
    "withheld-security",
    "outside-scope",
}

FORBIDDEN_PATTERNS = {
    "private IPv4 address": re.compile(
        r"\b(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3}|172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3})\b"
    ),
    "GitHub token": re.compile(r"\b(?:ghp|github_pat)_[A-Za-z0-9_]{20,}\b"),
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "Cloudflare token assignment": re.compile(
        r"(?i)\bCLOUDFLARE_(?:API_)?TOKEN\s*=\s*[^\s'\"]+"
    ),
    "generic secret assignment": re.compile(
        r"(?i)\b(?:password|passwd|secret|api[_-]?key|token)\s*=\s*['\"][^'\"]{8,}['\"]"
    ),
}

CYRILLIC = re.compile(r"[\u0400-\u052f]")
POSITIVE_AWARD_CLAIMS = (
    re.compile(r"(?i)\bngi fediversity (?:grant|funding) (?:was |has been )?(?:awarded|received|secured)\b"),
    re.compile(r"(?i)\bawarded (?:the )?ngi fediversity (?:grant|funding)\b"),
    re.compile(r"(?i)\bngi fediversity funded project\b"),
)

TEXT_SUFFIXES = {
    ".css",
    ".go",
    ".html",
    ".ini",
    ".js",
    ".json",
    ".md",
    ".nix",
    ".py",
    ".rego",
    ".sh",
    ".svg",
    ".toml",
    ".ts",
    ".txt",
    ".xml",
    ".yaml",
    ".yml",
}
TEXT_FILENAMES = {"LICENSE", "NOTICE", "go.mod", "go.sum"}
SKIPPED_PARTS = {".git", "node_modules", "result", "vendor"}


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def is_public_text(path: Path) -> bool:
    if not path.is_file() or any(part in SKIPPED_PARTS for part in path.parts):
        return False
    return path.suffix.lower() in TEXT_SUFFIXES or path.name in TEXT_FILENAMES


def load_json(relative_path: str) -> Any:
    return json.loads((ROOT / relative_path).read_text(encoding="utf-8"))


def validate_required_files() -> list[str]:
    return [
        f"missing required file: {path}"
        for path in REQUIRED_FILES
        if not (ROOT / path).is_file()
    ]


def validate_json_files() -> list[str]:
    errors: list[str] = []
    for path in sorted(ROOT.rglob("*.json")):
        if any(part in SKIPPED_PARTS for part in path.parts):
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            errors.append(f"invalid JSON {relative(path)}: {exc}")
    return errors


def validate_public_text() -> list[str]:
    errors: list[str] = []
    for path in sorted(ROOT.rglob("*")):
        if not is_public_text(path):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"cannot read {relative(path)}: {exc}")
            continue

        match = CYRILLIC.search(text)
        if match:
            line = text.count("\n", 0, match.start()) + 1
            errors.append(
                f"non-English Cyrillic text detected in {relative(path)}:{line}"
            )

        for label, pattern in FORBIDDEN_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"{label} detected in {relative(path)}")

        for pattern in POSITIVE_AWARD_CLAIMS:
            if pattern.search(text):
                errors.append(f"unverified NGI Fediversity award claim in {relative(path)}")

    return errors


def validate_machine_status() -> list[str]:
    errors: list[str] = []
    try:
        project = load_json("site-content/project.json")
        status = load_json("site-content/status.json")
        grant = load_json("site-content/grant.json")
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return [f"cannot validate machine-readable status: {exc}"]

    if project.get("openSource") is not True:
        errors.append("site-content/project.json must declare openSource=true")
    if project.get("productionReady") is not False:
        errors.append("site-content/project.json must not claim production readiness")
    if project.get("repository") != "https://github.com/claryel-company/claryel-boxcore":
        errors.append("site-content/project.json has an unexpected repository URL")

    capabilities = status.get("capabilities")
    if not isinstance(capabilities, list) or not capabilities:
        errors.append("site-content/status.json must contain a non-empty capabilities list")
    else:
        identifiers: set[str] = set()
        for index, capability in enumerate(capabilities):
            if not isinstance(capability, dict):
                errors.append(f"status capability {index} is not an object")
                continue
            identifier = capability.get("id")
            implementation_status = capability.get("status")
            if not isinstance(identifier, str) or not identifier:
                errors.append(f"status capability {index} has no id")
            elif identifier in identifiers:
                errors.append(f"duplicate status capability id: {identifier}")
            else:
                identifiers.add(identifier)
            if implementation_status not in IMPLEMENTATION_STATUSES:
                errors.append(
                    f"invalid implementation status for {identifier or index}: {implementation_status}"
                )

    if grant.get("programme") != "NGI Fediversity":
        errors.append("site-content/grant.json has an unexpected programme")
    if grant.get("requestedAmountEUR") != 50000:
        errors.append("site-content/grant.json must declare requestedAmountEUR=50000")
    if grant.get("fundingStatus") != "requested-not-awarded":
        errors.append("site-content/grant.json must declare requested-not-awarded")
    if grant.get("advanceRequested") is not False:
        errors.append("site-content/grant.json must declare advanceRequested=false")

    return errors


def validate_language_policy() -> list[str]:
    errors: list[str] = []
    policy = (ROOT / "docs/LANGUAGE_POLICY.md").read_text(encoding="utf-8")
    required_phrases = (
        "Public repositories are English-only",
        "User-facing website translations",
        "managed-web localisation",
    )
    for phrase in required_phrases:
        if phrase not in policy:
            errors.append(f"language policy is missing required phrase: {phrase}")
    return errors


def main() -> int:
    errors = [
        *validate_required_files(),
        *validate_json_files(),
        *validate_public_text(),
        *validate_machine_status(),
        *validate_language_policy(),
    ]
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("CLARYEL Box Core public baseline validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
