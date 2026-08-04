#!/usr/bin/env python3
"""Build a bounded repository knowledge payload without exposing credentials."""

from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
from typing import Any
import urllib.error
import urllib.parse
import urllib.request

PUBLISHER_VERSION = "project-knowledge-publisher-v1"
MAX_FILES = 4000
MAX_FILE_BYTES = 4 * 1024 * 1024
MAX_TOTAL_BYTES = 192 * 1024 * 1024
MAX_GITHUB_RECORDS = 100

SUPPORTED_BINARY_EXTENSIONS = {".pdf", ".docx", ".xlsx"}
SUPPORTED_TEXT_EXTENSIONS = {
    ".md",
    ".mdx",
    ".rst",
    ".txt",
    ".log",
    ".html",
    ".htm",
    ".json",
    ".jsonl",
    ".csv",
    ".tsv",
}
WRAPPED_TEXT_EXTENSIONS = {
    ".yaml",
    ".yml",
    ".toml",
    ".xml",
    ".sql",
    ".graphql",
    ".gql",
    ".proto",
    ".ini",
    ".cfg",
    ".conf",
}

DOCUMENT_BASENAMES = {
    "agents.md",
    "architecture.md",
    "changelog.md",
    "contributing.md",
    "decisions.md",
    "design.md",
    "documentation.md",
    "instructions.md",
    "license.md",
    "policy.md",
    "readme.md",
    "roadmap.md",
    "runbook.md",
    "security.md",
    "specification.md",
}

DOCUMENT_SEGMENTS = {
    "adr",
    "adrs",
    "architecture",
    "decision",
    "decisions",
    "design",
    "doc",
    "docs",
    "documentation",
    "guide",
    "guides",
    "instruction",
    "instructions",
    "manual",
    "manuals",
    "migration",
    "migrations",
    "openapi",
    "plan",
    "plans",
    "policies",
    "policy",
    "rfc",
    "rfcs",
    "risk",
    "risks",
    "roadmap",
    "runbook",
    "runbooks",
    "schema",
    "schemas",
    "spec",
    "specs",
    "standard",
    "standards",
}

EXCLUDED_SEGMENTS = {
    ".git",
    ".next",
    ".terraform",
    ".tox",
    ".venv",
    "__pycache__",
    "artifacts",
    "build",
    "cache",
    "coverage",
    "dist",
    "generated",
    "models",
    "node_modules",
    "target",
    "vendor",
    "weights",
}

EXCLUDED_SUFFIXES = {
    ".7z",
    ".bin",
    ".ckpt",
    ".dmg",
    ".env",
    ".gguf",
    ".iso",
    ".key",
    ".onnx",
    ".p12",
    ".pem",
    ".pt",
    ".pth",
    ".safetensors",
    ".tar",
    ".tgz",
    ".zip",
}

SECRET_PATH_PATTERN = re.compile(
    r"(^|/)(?:\.env(?:\.|$)|id_(?:rsa|dsa|ecdsa|ed25519)(?:\.|$)|"
    r"credentials?(?:\.|/|$)|secrets?(?:\.|/|$)|private[-_]?keys?(?:\.|/|$))",
    re.IGNORECASE,
)
PRIVATE_KEY_PATTERN = re.compile(
    r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----.*?-----END [A-Z0-9 ]*PRIVATE KEY-----",
    re.DOTALL,
)
ASSIGNMENT_SECRET_PATTERN = re.compile(
    r"(?im)^(\s*(?:password|passwd|token|api[_-]?key|client[_-]?secret|secret)\s*[:=]\s*)"
    r"([^\s#][^\r\n]{7,})$"
)
BEARER_PATTERN = re.compile(r"(?i)(authorization\s*:\s*bearer\s+)[A-Za-z0-9._~+\-/=]{8,}")
GITHUB_TOKEN_PATTERN = re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{40,})\b")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def run_git(*args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        check=True,
        capture_output=True,
        text=True,
        timeout=60,
    )
    return completed.stdout.strip()


def tracked_files() -> list[str]:
    completed = subprocess.run(
        ["git", "ls-files", "-z"],
        check=True,
        capture_output=True,
        timeout=120,
    )
    return [item.decode("utf-8", errors="surrogateescape") for item in completed.stdout.split(b"\0") if item]


def should_include(path_value: str) -> bool:
    path = PurePosixPath(path_value)
    lowered_parts = [part.casefold() for part in path.parts]
    lowered = path_value.casefold()
    basename = path.name.casefold()
    suffix = path.suffix.casefold()

    if any(part in EXCLUDED_SEGMENTS for part in lowered_parts):
        return False
    if suffix in EXCLUDED_SUFFIXES or SECRET_PATH_PATTERN.search(lowered):
        return False
    if basename.startswith("readme") or basename in DOCUMENT_BASENAMES:
        return True
    if any(part in DOCUMENT_SEGMENTS for part in lowered_parts):
        return suffix in SUPPORTED_TEXT_EXTENSIONS | SUPPORTED_BINARY_EXTENSIONS | WRAPPED_TEXT_EXTENSIONS
    if path.parts[:2] == (".github", "workflows"):
        return suffix in {".yaml", ".yml"}
    if basename.startswith(("compose.", "docker-compose.")):
        return suffix in {".yaml", ".yml"}
    if basename in {"openapi.yaml", "openapi.yml", "openapi.json", "agent-context.yaml", "agent-context.yml"}:
        return True
    return False


def redact_text(text: str) -> tuple[str, int]:
    redactions = 0

    def private_key_replacement(match: re.Match[str]) -> str:
        nonlocal redactions
        redactions += 1
        return "[REDACTED PRIVATE KEY]"

    def assignment_replacement(match: re.Match[str]) -> str:
        nonlocal redactions
        value = match.group(2).strip()
        if value.startswith(("${", "{{", "<", "[REDACTED", "example", "changeme")):
            return match.group(0)
        redactions += 1
        return match.group(1) + "[REDACTED]"

    text = PRIVATE_KEY_PATTERN.sub(private_key_replacement, text)
    text, count = BEARER_PATTERN.subn(r"\1[REDACTED]", text)
    redactions += count
    text, count = GITHUB_TOKEN_PATTERN.subn("[REDACTED GITHUB TOKEN]", text)
    redactions += count
    text = ASSIGNMENT_SECRET_PATTERN.sub(assignment_replacement, text)
    return text, redactions


def decode_text(data: bytes) -> str:
    for encoding in ("utf-8-sig", "utf-8", "utf-16", "cp1252"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    raise ValueError("unsupported text encoding")


def first_title_and_summary(text: str, fallback: str) -> tuple[str, str]:
    title = fallback
    summary_parts: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            if summary_parts:
                break
            continue
        if stripped.startswith("#") and title == fallback:
            candidate = stripped.lstrip("#").strip()
            if candidate:
                title = candidate[:300]
            continue
        if stripped.startswith(("```", "---", "<!--")):
            continue
        summary_parts.append(stripped)
        if sum(len(item) for item in summary_parts) >= 700:
            break
    summary = " ".join(summary_parts)[:1000] or f"Documentation source {fallback}"
    return title, summary


def category_for(path_value: str) -> str:
    lowered = path_value.casefold()
    if "/adr/" in f"/{lowered}" or "/decisions/" in f"/{lowered}" or "decision" in PurePosixPath(lowered).name:
        return "decision"
    if "architecture" in lowered or "/design/" in f"/{lowered}":
        return "architecture"
    if "runbook" in lowered or "/manual" in f"/{lowered}":
        return "runbook"
    if "roadmap" in lowered or "/plans/" in f"/{lowered}":
        return "roadmap"
    if "risk" in lowered:
        return "risk"
    if "policy" in lowered or "standard" in lowered:
        return "standard"
    if "migration" in lowered or PurePosixPath(lowered).suffix == ".sql":
        return "schema"
    if "openapi" in lowered or PurePosixPath(lowered).suffix in {".proto", ".graphql", ".gql"}:
        return "api"
    if PurePosixPath(lowered).name.startswith(("compose.", "docker-compose.")):
        return "schema"
    if PurePosixPath(lowered).parts[:2] == (".github", "workflows"):
        return "instruction"
    return "documentation"


def github_json(token: str, url: str) -> Any:
    request = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "claryel-project-knowledge-publisher",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"GitHub API returned HTTP {exc.code} for a repository-local read") from exc


def render_records(title: str, intro: str, records: list[dict[str, Any]]) -> bytes:
    lines = [f"# {title}", "", intro, ""]
    if not records:
        lines.append("No matching records were returned at synchronization time.")
    for record in records:
        lines.extend([f"## {record.get('title') or record.get('name') or record.get('tag_name') or 'Untitled'}", ""])
        for key in ("number", "state", "draft", "created_at", "updated_at", "closed_at", "published_at", "html_url"):
            if record.get(key) is not None:
                lines.append(f"- {key}: {record.get(key)}")
        labels = [item.get("name") for item in record.get("labels") or [] if isinstance(item, dict) and item.get("name")]
        assignees = [item.get("login") for item in record.get("assignees") or [] if isinstance(item, dict) and item.get("login")]
        if labels:
            lines.append(f"- labels: {', '.join(labels)}")
        if assignees:
            lines.append(f"- assignees: {', '.join(assignees)}")
        lines.extend(["", str(record.get("body") or record.get("description") or "No description provided."), ""])
    text, _ = redact_text("\n".join(lines) + "\n")
    return text.encode("utf-8")


def write_generated_entry(
    *,
    payload_root: Path,
    manifest_entries: list[dict[str, Any]],
    repository: str,
    revision: str,
    source_path: str,
    filename: str,
    content: bytes,
    title: str,
    summary: str,
    category: str,
    source_kind: str,
    records: list[dict[str, Any]] | None = None,
) -> None:
    target = payload_root / "generated" / filename
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(content)
    manifest_entries.append(
        {
            "source_key": f"{source_kind}:{repository}:{source_path}",
            "source_kind": source_kind,
            "source_path": source_path,
            "source_uri": f"https://github.com/{repository}/{source_path}",
            "payload_path": str(target.relative_to(payload_root.parent)),
            "upload_filename": filename,
            "source_content_sha256": sha256_bytes(content),
            "indexed_content_sha256": sha256_bytes(content),
            "source_revision": revision,
            "title": title,
            "summary": summary,
            "category": category,
            "size_bytes": len(content),
            "redactions": 0,
            "generated": True,
            "records": records or [],
        }
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--revision", required=True)
    parser.add_argument("--default-branch", required=True)
    parser.add_argument("--visibility", choices=("public", "private"), required=True)
    parser.add_argument("--github-token", required=True)
    args = parser.parse_args()

    output = Path(args.output).resolve()
    payload_root = output / "payload"
    payload_root.mkdir(parents=True, exist_ok=True)
    entries: list[dict[str, Any]] = []
    total_bytes = 0
    total_redactions = 0

    files = [path for path in tracked_files() if should_include(path)]
    if len(files) > MAX_FILES:
        raise SystemExit(f"candidate file count {len(files)} exceeds {MAX_FILES}")

    for source_path in sorted(files):
        source = Path(source_path)
        try:
            data = source.read_bytes()
        except OSError as exc:
            raise SystemExit(f"cannot read tracked source {source_path}: {exc}") from exc
        if not data or len(data) > MAX_FILE_BYTES:
            continue
        suffix = source.suffix.casefold()
        original_sha = sha256_bytes(data)
        redactions = 0
        title = source_path
        summary = f"Repository source {source_path}"
        upload_filename = source.name
        indexed_data = data

        if suffix in SUPPORTED_TEXT_EXTENSIONS | WRAPPED_TEXT_EXTENSIONS:
            try:
                text = decode_text(data)
            except ValueError:
                continue
            text, redactions = redact_text(text)
            title, summary = first_title_and_summary(text, source_path)
            if suffix in WRAPPED_TEXT_EXTENSIONS or suffix == ".mdx":
                language = suffix.lstrip(".") or "text"
                wrapped = (
                    f"# {title}\n\n"
                    f"Source repository: {args.repository}\n\n"
                    f"Source path: `{source_path}`\n\n"
                    f"Source revision: `{args.revision}`\n\n"
                    f"Source SHA-256: `{original_sha}`\n\n"
                    f"```{language}\n{text}\n```\n"
                )
                indexed_data = wrapped.encode("utf-8")
                upload_filename = source.name + ".md"
            else:
                indexed_data = text.encode("utf-8")
        elif suffix not in SUPPORTED_BINARY_EXTENSIONS:
            continue

        total_bytes += len(indexed_data)
        total_redactions += redactions
        if total_bytes > MAX_TOTAL_BYTES:
            raise SystemExit(f"indexed payload exceeds {MAX_TOTAL_BYTES} bytes")
        target = payload_root / "files" / PurePosixPath(source_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(indexed_data)
        entries.append(
            {
                "source_key": f"github-file:{args.repository}:{source_path}",
                "source_kind": "github-file",
                "source_path": source_path,
                "source_uri": f"https://github.com/{args.repository}/blob/{args.revision}/{urllib.parse.quote(source_path)}",
                "payload_path": str(target.relative_to(output)),
                "upload_filename": upload_filename,
                "source_content_sha256": original_sha,
                "indexed_content_sha256": sha256_bytes(indexed_data),
                "source_revision": args.revision,
                "title": title,
                "summary": summary,
                "category": category_for(source_path),
                "size_bytes": len(indexed_data),
                "redactions": redactions,
                "generated": False,
                "records": [],
            }
        )

    api_base = f"https://api.github.com/repos/{args.repository}"
    repository_data = github_json(args.github_token, api_base)
    issue_data = [
        item
        for item in github_json(
            args.github_token,
            api_base + "/issues?state=all&sort=updated&direction=desc&per_page=100",
        )
        if "pull_request" not in item
    ][:MAX_GITHUB_RECORDS]
    pull_data = github_json(
        args.github_token,
        api_base + "/pulls?state=all&sort=updated&direction=desc&per_page=100",
    )[:MAX_GITHUB_RECORDS]
    release_data = github_json(args.github_token, api_base + "/releases?per_page=100")[:MAX_GITHUB_RECORDS]

    metadata_content = render_records(
        f"{args.repository} repository context",
        "Current repository metadata captured by the repository-local publisher.",
        [
            {
                "title": repository_data.get("name"),
                "state": "archived" if repository_data.get("archived") else "active",
                "updated_at": repository_data.get("updated_at"),
                "html_url": repository_data.get("html_url"),
                "body": repository_data.get("description") or "No repository description provided.",
            }
        ],
    )
    readme_entries = [item for item in entries if PurePosixPath(item["source_path"]).name.casefold().startswith("readme")]
    mission = (readme_entries[0]["summary"] if readme_entries else repository_data.get("description")) or f"Project repository {args.repository}"
    write_generated_entry(
        payload_root=payload_root,
        manifest_entries=entries,
        repository=args.repository,
        revision=args.revision,
        source_path="repository/context",
        filename="repository-context.md",
        content=metadata_content,
        title=f"{args.repository} repository context",
        summary=str(mission)[:1000],
        category="repository-context",
        source_kind="github-repository",
        records=[],
    )
    write_generated_entry(
        payload_root=payload_root,
        manifest_entries=entries,
        repository=args.repository,
        revision=args.revision,
        source_path="issues",
        filename="github-issues.md",
        content=render_records(
            f"{args.repository} issues",
            "Current and recently updated GitHub issues. Open issues are projected into the operational backlog.",
            issue_data,
        ),
        title=f"{args.repository} GitHub issues",
        summary=f"{len(issue_data)} current and recently updated issue records",
        category="issues",
        source_kind="github-issue",
        records=issue_data,
    )
    write_generated_entry(
        payload_root=payload_root,
        manifest_entries=entries,
        repository=args.repository,
        revision=args.revision,
        source_path="pull-requests",
        filename="github-pull-requests.md",
        content=render_records(
            f"{args.repository} pull requests",
            "Current and recently updated pull requests, including their rationale and status.",
            pull_data,
        ),
        title=f"{args.repository} pull requests",
        summary=f"{len(pull_data)} current and recently updated pull request records",
        category="pull-requests",
        source_kind="github-pull-request",
        records=pull_data,
    )
    write_generated_entry(
        payload_root=payload_root,
        manifest_entries=entries,
        repository=args.repository,
        revision=args.revision,
        source_path="releases",
        filename="github-releases.md",
        content=render_records(
            f"{args.repository} releases",
            "Published GitHub releases and release notes.",
            release_data,
        ),
        title=f"{args.repository} releases",
        summary=f"{len(release_data)} release records",
        category="releases",
        source_kind="github-release",
        records=release_data,
    )

    manifest = {
        "schema_version": 1,
        "publisher_version": PUBLISHER_VERSION,
        "repository": args.repository,
        "revision": args.revision,
        "default_branch": args.default_branch,
        "visibility": args.visibility,
        "privacy_label": "PUBLIC" if args.visibility == "public" else "INTERNAL",
        "source_channel": f"github-sync:{args.repository}"[:100],
        "retention_days": 730,
        "mission": str(mission)[:1000],
        "repository_archived": bool(repository_data.get("archived")),
        "repository_html_url": repository_data.get("html_url"),
        "entries": entries,
        "statistics": {
            "tracked_files": len(tracked_files()),
            "selected_files": len(files),
            "published_sources": len(entries),
            "indexed_bytes": total_bytes,
            "redactions": total_redactions,
            "issues": len(issue_data),
            "pull_requests": len(pull_data),
            "releases": len(release_data),
        },
    }
    (output / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "repository": args.repository,
                "revision": args.revision,
                "published_sources": len(entries),
                "indexed_bytes": total_bytes,
                "redactions": total_redactions,
            }
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"collector_error={type(exc).__name__}: {exc}", file=sys.stderr)
        raise
