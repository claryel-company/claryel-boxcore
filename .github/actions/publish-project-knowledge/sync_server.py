#!/usr/bin/env python3
"""Synchronise a repository payload into PostgreSQL, encrypted storage and Qdrant.

This program runs inside the governed Agent Fabric container. It never prints
credentials or source text. Every logical source is switched independently only
after the new document has passed Knowledge API ingestion.
"""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
import json
import mimetypes
import os
from pathlib import Path, PurePosixPath
import re
import sys
from typing import Any
from uuid import UUID

import httpx
import psycopg
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb

PUBLISHER_VERSION = "project-knowledge-publisher-v1"
KNOWLEDGE_API_URL = "http://knowledge-api:8082"
AGENT_TOKEN_ENV = "CLARYEL_CONTEXT_API_TOKEN"
DATABASE_URL_ENV = "CLARYEL_DATABASE_URL"
SUPPORTED_UPLOAD_SUFFIXES = {
    ".txt",
    ".md",
    ".rst",
    ".log",
    ".html",
    ".htm",
    ".json",
    ".jsonl",
    ".csv",
    ".tsv",
    ".pdf",
    ".docx",
    ".xlsx",
}


class SyncError(RuntimeError):
    pass


def utc_now() -> datetime:
    return datetime.now(UTC)


def safe_json(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, (datetime, UUID)):
        return str(value)
    if isinstance(value, dict):
        return {str(key): safe_json(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [safe_json(item) for item in value]
    return str(value)


def require_manifest(root: Path) -> dict[str, Any]:
    manifest_path = root / "manifest.json"
    if not manifest_path.is_file():
        raise SyncError("manifest.json is missing")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    required = {
        "publisher_version",
        "repository",
        "revision",
        "default_branch",
        "visibility",
        "privacy_label",
        "source_channel",
        "retention_days",
        "entries",
    }
    missing = required - set(manifest)
    if missing:
        raise SyncError(f"manifest fields are missing: {sorted(missing)}")
    if manifest["publisher_version"] != PUBLISHER_VERSION:
        raise SyncError("unsupported publisher version")
    if not re.fullmatch(r"claryel-company/[A-Za-z0-9_.-]+", str(manifest["repository"])):
        raise SyncError("invalid repository identifier")
    if not re.fullmatch(r"[0-9a-f]{40}", str(manifest["revision"])):
        raise SyncError("repository revision must be a full commit SHA")
    if manifest["visibility"] not in {"public", "private"}:
        raise SyncError("invalid repository visibility")
    if manifest["privacy_label"] not in {"PUBLIC", "INTERNAL"}:
        raise SyncError("invalid repository privacy label")
    if bool(manifest.get("repository_archived")):
        raise SyncError("archived repositories cannot publish into the active knowledge scope")
    entries = manifest["entries"]
    if not isinstance(entries, list) or not entries:
        raise SyncError("repository payload contains no sources")
    return manifest


def api_headers() -> dict[str, str]:
    token = os.environ.get(AGENT_TOKEN_ENV, "")
    if len(token) < 16:
        raise SyncError("local Knowledge API token is unavailable")
    return {"Authorization": f"Bearer {token}"}


def upload_document(
    *,
    path: Path,
    upload_filename: str,
    privacy_label: str,
    retention_days: int,
    source_channel: str,
) -> dict[str, Any]:
    if not path.is_file() or not path.stat().st_size:
        raise SyncError("source payload is empty or missing")
    suffix = Path(upload_filename).suffix.casefold()
    if suffix not in SUPPORTED_UPLOAD_SUFFIXES:
        raise SyncError(f"unsupported upload suffix: {suffix}")
    content_type = mimetypes.guess_type(upload_filename)[0] or "application/octet-stream"
    with path.open("rb") as handle:
        response = httpx.post(
            f"{KNOWLEDGE_API_URL}/v1/knowledge/documents",
            headers=api_headers(),
            files={"file": (upload_filename, handle, content_type)},
            data={
                "privacy_label": privacy_label,
                "retention_days": str(retention_days),
                "source_channel": source_channel,
            },
            timeout=900,
        )
    response.raise_for_status()
    payload = response.json()
    if payload.get("status") not in {"ready", "duplicate"}:
        raise SyncError("Knowledge API did not accept the source")
    if not payload.get("document_id") or int(payload.get("chunk_count") or 0) < 1:
        raise SyncError("accepted source has no document or chunks")
    if payload.get("embedding_model") != "nomic-embed-text":
        raise SyncError("source was not embedded by the accepted local model")
    if payload.get("encrypted_at_rest") is not True:
        raise SyncError("source was not encrypted at rest")
    if payload.get("malware_scan") != "clean":
        raise SyncError("source did not pass malware scanning")
    return payload


def delete_document(document_id: str, *, purge_object: bool, reason: str) -> None:
    response = httpx.delete(
        f"{KNOWLEDGE_API_URL}/v1/knowledge/documents/{document_id}",
        headers=api_headers(),
        params={"purge_object": str(purge_object).lower(), "reason": reason},
        timeout=300,
    )
    if response.status_code == 404:
        return
    response.raise_for_status()


def privacy_label_id(cursor: psycopg.Cursor[Any], label_key: str) -> UUID:
    cursor.execute("SELECT id FROM privacy_labels WHERE label_key = %s", (label_key,))
    row = cursor.fetchone()
    if row is None:
        raise SyncError(f"privacy label is missing: {label_key}")
    return row["id"]


def verify_repository_scope(cursor: psycopg.Cursor[Any], repository: str) -> None:
    cursor.execute("SELECT 1 FROM active_repository_scope WHERE repository = %s", (repository,))
    if cursor.fetchone() is None:
        raise SyncError("repository is outside the active repository scope")


def verify_schema(cursor: psycopg.Cursor[Any]) -> None:
    required = {
        "knowledge_sync_runs",
        "knowledge_sources",
        "knowledge_source_versions",
        "knowledge_source_projections",
        "website_crawl_policies",
    }
    cursor.execute(
        "SELECT table_name FROM information_schema.tables "
        "WHERE table_schema='public' AND table_name = ANY(%s)",
        (list(required),),
    )
    present = {row["table_name"] for row in cursor.fetchall()}
    if present != required:
        raise SyncError(f"knowledge source schema is incomplete: {sorted(required - present)}")


def start_run(
    connection: psycopg.Connection[Any],
    *,
    run_key: str,
    repository: str,
    revision: str,
    manifest: dict[str, Any],
) -> UUID:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO knowledge_sync_runs (
                run_key, trigger_kind, scope_kind, repository, source_revision,
                status, metadata
            ) VALUES (%s, %s, 'repository', %s, %s, 'running', %s)
            ON CONFLICT (run_key) DO UPDATE
            SET status = 'running',
                started_at = now(),
                completed_at = NULL,
                error_summary = NULL,
                metadata = EXCLUDED.metadata
            RETURNING id
            """,
            (
                run_key,
                str(manifest.get("trigger_kind") or "reconcile"),
                repository,
                revision,
                Jsonb(
                    {
                        "publisher_version": PUBLISHER_VERSION,
                        "default_branch": manifest["default_branch"],
                        "visibility": manifest["visibility"],
                        "statistics": manifest.get("statistics") or {},
                    }
                ),
            ),
        )
        run_id = cursor.fetchone()["id"]
    connection.commit()
    return run_id


def finish_run(
    connection: psycopg.Connection[Any],
    *,
    run_id: UUID,
    status: str,
    counts: dict[str, int],
    error_summary: str | None = None,
) -> None:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            UPDATE knowledge_sync_runs
            SET status = %s,
                completed_at = now(),
                discovered_count = %s,
                unchanged_count = %s,
                created_count = %s,
                updated_count = %s,
                missing_count = %s,
                failed_count = %s,
                error_summary = %s
            WHERE id = %s
            """,
            (
                status,
                counts["discovered"],
                counts["unchanged"],
                counts["created"],
                counts["updated"],
                counts["missing"],
                counts["failed"],
                error_summary,
                run_id,
            ),
        )
    connection.commit()


def projection_kind(category: str) -> str:
    return {
        "repository-context": "repository-context",
        "decision": "decision",
        "architecture": "architecture-record",
        "runbook": "instruction",
        "roadmap": "project-status",
        "risk": "risk",
        "standard": "instruction",
        "schema": "schema-asset",
        "api": "schema-asset",
        "issues": "next-step",
        "pull-requests": "decision",
        "releases": "project-status",
        "instruction": "instruction",
        "documentation": "instruction",
    }.get(category, "instruction")


def architecture_record_type(category: str) -> str | None:
    return {
        "decision": "decision",
        "architecture": "architecture",
        "runbook": "runbook",
        "roadmap": "roadmap",
        "risk": "risk",
        "standard": "standard",
    }.get(category)


def architecture_status(category: str) -> str:
    return {
        "runbook": "operating",
        "roadmap": "proposed",
        "risk": "captured",
    }.get(category, "accepted")


def schema_asset_type(entry: dict[str, Any]) -> str:
    path = str(entry.get("source_path") or "").casefold()
    if entry.get("category") == "api":
        return "api"
    if "migration" in path or path.endswith(".sql"):
        return "migration"
    if "policy" in path:
        return "policy"
    return "schema"


def upsert_repository_context(
    cursor: psycopg.Cursor[Any],
    *,
    manifest: dict[str, Any],
    entry: dict[str, Any],
    label_id: UUID,
) -> UUID:
    repository = manifest["repository"]
    cursor.execute("UPDATE repository_contexts SET active=false WHERE repository=%s AND active=true", (repository,))
    cursor.execute(
        """
        INSERT INTO repository_contexts (
            repository, visibility, owner_repository, mission, ideology,
            trust_boundaries, prohibited_disclosures, manifest,
            source_commit, content_sha256, active
        ) VALUES (%s, %s, %s, %s, '[]'::jsonb, '[]'::jsonb, '[]'::jsonb,
                  %s, %s, %s, true)
        ON CONFLICT (repository, source_commit, content_sha256) DO UPDATE
        SET active=true, recorded_at=now(), manifest=EXCLUDED.manifest
        RETURNING id
        """,
        (
            repository,
            manifest["visibility"],
            repository,
            str(manifest.get("mission") or entry.get("summary") or repository)[:4000],
            Jsonb(
                {
                    "publisher_version": PUBLISHER_VERSION,
                    "default_branch": manifest["default_branch"],
                    "revision": manifest["revision"],
                    "source_count": len(manifest["entries"]),
                    "privacy_label_id": str(label_id),
                }
            ),
            manifest["revision"],
            entry["source_content_sha256"],
        ),
    )
    return cursor.fetchone()["id"]


def upsert_architecture_record(
    cursor: psycopg.Cursor[Any],
    *,
    manifest: dict[str, Any],
    entry: dict[str, Any],
    label_id: UUID,
) -> UUID | None:
    record_type = architecture_record_type(str(entry.get("category") or ""))
    if record_type is None or bool(entry.get("generated")):
        return None
    repository = manifest["repository"]
    record_key = f"github:{repository}:{entry['source_path']}"
    cursor.execute(
        "SELECT id, current_version FROM architecture_records WHERE record_key=%s FOR UPDATE",
        (record_key,),
    )
    existing = cursor.fetchone()
    next_version = int(existing["current_version"]) + 1 if existing else 1
    if existing:
        cursor.execute(
            """
            UPDATE architecture_records
            SET record_type=%s, title=%s, purpose=%s, accountable_repository=%s,
                status=%s, privacy_label_id=%s, current_version=%s, updated_at=now()
            WHERE id=%s
            """,
            (
                record_type,
                str(entry.get("title") or entry["source_path"])[:1000],
                str(entry.get("summary") or "Imported repository architecture source")[:8000],
                repository,
                architecture_status(str(entry.get("category") or "")),
                label_id,
                next_version,
                existing["id"],
            ),
        )
        record_id = existing["id"]
    else:
        cursor.execute(
            """
            INSERT INTO architecture_records (
                record_key, record_type, title, purpose, accountable_repository,
                status, privacy_label_id, current_version
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, 1)
            RETURNING id
            """,
            (
                record_key,
                record_type,
                str(entry.get("title") or entry["source_path"])[:1000],
                str(entry.get("summary") or "Imported repository architecture source")[:8000],
                repository,
                architecture_status(str(entry.get("category") or "")),
                label_id,
            ),
        )
        record_id = cursor.fetchone()["id"]
    cursor.execute(
        """
        INSERT INTO architecture_record_versions (
            architecture_record_id, version_number, original_intent,
            verified_facts, assumptions, unknowns, constraints, current_state,
            decision, alternatives, consequences, planned_evolution,
            implementation_status, acceptance_criteria, evidence,
            rollback_or_forward_recovery, review_triggers,
            source_repository, source_path, source_commit, content_sha256
        ) VALUES (
            %s, %s, %s, '[]'::jsonb, '[]'::jsonb, '[]'::jsonb, '[]'::jsonb, %s,
            %s, '[]'::jsonb, '[]'::jsonb, '[]'::jsonb,
            %s, '[]'::jsonb, %s, NULL, '[]'::jsonb,
            %s, %s, %s, %s
        )
        ON CONFLICT (source_repository, source_path, source_commit, content_sha256)
        DO NOTHING
        """,
        (
            record_id,
            next_version,
            str(entry.get("summary") or "")[:8000],
            str(entry.get("summary") or "")[:8000],
            str(entry.get("summary") or "")[:8000] if record_type == "decision" else None,
            Jsonb({"publisher_version": PUBLISHER_VERSION, "category": entry.get("category")}),
            Jsonb(
                [
                    {
                        "source_uri": entry.get("source_uri"),
                        "source_sha256": entry.get("source_content_sha256"),
                    }
                ]
            ),
            repository,
            entry["source_path"],
            manifest["revision"],
            entry["source_content_sha256"],
        ),
    )
    return record_id


def upsert_schema_asset(
    cursor: psycopg.Cursor[Any],
    *,
    manifest: dict[str, Any],
    entry: dict[str, Any],
    label_id: UUID,
) -> UUID | None:
    if entry.get("category") not in {"schema", "api"} or bool(entry.get("generated")):
        return None
    repository = manifest["repository"]
    asset_type = schema_asset_type(entry)
    asset_name = str(entry["source_path"])
    cursor.execute(
        """
        UPDATE schema_assets SET active=false
        WHERE authority_repository=%s AND data_domain='repository'
          AND asset_type=%s AND asset_name=%s AND active=true
        """,
        (repository, asset_type, asset_name),
    )
    cursor.execute(
        """
        INSERT INTO schema_assets (
            authority_repository, data_domain, asset_type, asset_name,
            definition, privacy_label_id, source_path, source_commit,
            content_sha256, active
        ) VALUES (%s, 'repository', %s, %s, %s, %s, %s, %s, %s, true)
        ON CONFLICT (authority_repository, data_domain, asset_type, asset_name, source_commit)
        DO UPDATE SET definition=EXCLUDED.definition,
                      privacy_label_id=EXCLUDED.privacy_label_id,
                      content_sha256=EXCLUDED.content_sha256,
                      active=true,
                      recorded_at=now()
        RETURNING id
        """,
        (
            repository,
            asset_type,
            asset_name,
            Jsonb(
                {
                    "publisher_version": PUBLISHER_VERSION,
                    "title": entry.get("title"),
                    "summary": entry.get("summary"),
                    "source_uri": entry.get("source_uri"),
                }
            ),
            label_id,
            asset_name,
            manifest["revision"],
            entry["source_content_sha256"],
        ),
    )
    return cursor.fetchone()["id"]


def issue_priority(labels: list[str]) -> tuple[str, int]:
    lowered = {item.casefold().replace("_", "-") for item in labels}
    if lowered & {"p0", "priority:p0", "critical", "urgent"}:
        return "P0", 95
    if lowered & {"p1", "priority:p1", "high-priority", "high"}:
        return "P1", 80
    if lowered & {"p3", "priority:p3", "low-priority", "low"}:
        return "P3", 25
    return "P2", 55


def extract_acceptance_criteria(body: str) -> list[str]:
    criteria: list[str] = []
    for line in body.splitlines():
        stripped = line.strip()
        if re.match(r"^[-*]\s+\[[ xX]\]\s+", stripped):
            criteria.append(re.sub(r"^[-*]\s+\[[ xX]\]\s+", "", stripped)[:1000])
    return criteria[:50]


def upsert_issue_steps(
    cursor: psycopg.Cursor[Any],
    *,
    manifest: dict[str, Any],
    entry: dict[str, Any],
) -> int:
    if entry.get("category") != "issues":
        return 0
    repository = manifest["repository"]
    count = 0
    for issue in entry.get("records") or []:
        number = issue.get("number")
        if not isinstance(number, int):
            continue
        labels = [
            str(item.get("name"))
            for item in issue.get("labels") or []
            if isinstance(item, dict) and item.get("name")
        ]
        assignees = [
            str(item.get("login"))
            for item in issue.get("assignees") or []
            if isinstance(item, dict) and item.get("login")
        ]
        priority, urgency = issue_priority(labels)
        state = str(issue.get("state") or "open")
        blocked = any(item.casefold() in {"blocked", "status:blocked"} for item in labels)
        status = "done" if state == "closed" else ("blocked" if blocked else "planned")
        body = str(issue.get("body") or "")
        step_key = f"github-issue:{repository}#{number}"
        cursor.execute(
            """
            INSERT INTO next_steps (
                step_key, repository, title, purpose, priority, urgency_score,
                status, owner, supporting_owners, affected_domains,
                related_adrs, prerequisites, acceptance_criteria, validation,
                rollback, due_at, review_at, source_repository, source_path,
                source_commit, notification_policy, completed_at, updated_at
            ) VALUES (
                %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s,
                '[]'::jsonb, '[]'::jsonb, %s, '[]'::jsonb,
                NULL, NULL, NULL, %s, %s,
                %s, '{}'::jsonb, %s, now()
            )
            ON CONFLICT (step_key) DO UPDATE
            SET title=EXCLUDED.title,
                purpose=EXCLUDED.purpose,
                priority=EXCLUDED.priority,
                urgency_score=EXCLUDED.urgency_score,
                status=EXCLUDED.status,
                owner=EXCLUDED.owner,
                supporting_owners=EXCLUDED.supporting_owners,
                affected_domains=EXCLUDED.affected_domains,
                acceptance_criteria=EXCLUDED.acceptance_criteria,
                source_repository=EXCLUDED.source_repository,
                source_path=EXCLUDED.source_path,
                source_commit=EXCLUDED.source_commit,
                completed_at=EXCLUDED.completed_at,
                updated_at=now()
            """,
            (
                step_key,
                repository,
                str(issue.get("title") or f"Issue {number}")[:1000],
                (body[:8000] or f"GitHub issue {number}"),
                priority,
                urgency,
                status,
                assignees[0] if assignees else repository,
                Jsonb(assignees[1:]),
                Jsonb(labels),
                Jsonb(extract_acceptance_criteria(body)),
                repository,
                f"github/issues/{number}",
                manifest["revision"],
                issue.get("closed_at") if state == "closed" else None,
            ),
        )
        count += 1
    return count


def synchronise_entry(
    *,
    database_url: str,
    root: Path,
    manifest: dict[str, Any],
    entry: dict[str, Any],
    run_id: UUID,
) -> tuple[str, str | None, bool]:
    repository = manifest["repository"]
    source_key = str(entry.get("source_key") or "")
    source_path = str(entry.get("source_path") or "")
    if not source_key or not source_path:
        raise SyncError("source key or path is missing")
    payload_path = (root / str(entry.get("payload_path") or "")).resolve()
    if root not in payload_path.parents or not payload_path.is_file():
        raise SyncError("source payload path escapes the publication root")
    source_hash = str(entry.get("source_content_sha256") or "")
    indexed_hash = str(entry.get("indexed_content_sha256") or "")
    if not re.fullmatch(r"[0-9a-f]{64}", source_hash) or not re.fullmatch(r"[0-9a-f]{64}", indexed_hash):
        raise SyncError("source hash is invalid")

    with psycopg.connect(database_url, row_factory=dict_row, connect_timeout=10) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, current_document_id, current_version,
                       current_content_sha256, lifecycle_status
                FROM knowledge_sources
                WHERE source_key=%s
                """,
                (source_key,),
            )
            current = cursor.fetchone()
            if current and current["current_content_sha256"] == source_hash and current["lifecycle_status"] == "active":
                cursor.execute(
                    """
                    UPDATE knowledge_sources
                    SET last_seen_at=now(), last_sync_run_id=%s,
                        failure_count=0, last_error=NULL, updated_at=now()
                    WHERE id=%s
                    """,
                    (run_id, current["id"]),
                )
                connection.commit()
                return "unchanged", str(current["current_document_id"]), False

    upload = upload_document(
        path=payload_path,
        upload_filename=str(entry.get("upload_filename") or PurePosixPath(source_path).name),
        privacy_label=manifest["privacy_label"],
        retention_days=int(manifest["retention_days"]),
        source_channel=manifest["source_channel"],
    )
    new_document_id = str(upload["document_id"])
    created_document = upload.get("status") == "ready"
    old_document_id: str | None = None
    old_document_managed = False
    source_version_id: UUID | None = None

    try:
        with psycopg.connect(database_url, row_factory=dict_row, connect_timeout=10) as connection:
            with connection.cursor() as cursor:
                label_id = privacy_label_id(cursor, manifest["privacy_label"])
                cursor.execute(
                    """
                    SELECT id, current_document_id, current_version,
                           current_content_sha256, lifecycle_status
                    FROM knowledge_sources
                    WHERE source_key=%s
                    FOR UPDATE
                    """,
                    (source_key,),
                )
                current = cursor.fetchone()
                if current and current["current_content_sha256"] == source_hash and current["lifecycle_status"] == "active":
                    cursor.execute(
                        "UPDATE knowledge_sources SET last_seen_at=now(), last_sync_run_id=%s, updated_at=now() WHERE id=%s",
                        (run_id, current["id"]),
                    )
                    connection.commit()
                    if created_document and new_document_id != str(current["current_document_id"]):
                        delete_document(
                            new_document_id,
                            purge_object=True,
                            reason="concurrent-repository-source-duplicate",
                        )
                    return "unchanged", str(current["current_document_id"]), False

                if current:
                    source_id = current["id"]
                    next_version = int(current["current_version"]) + 1
                    old_document_id = str(current["current_document_id"]) if current["current_document_id"] else None
                    cursor.execute(
                        """
                        SELECT COALESCE((metadata->>'document_created_by_publisher')::boolean, false) AS managed
                        FROM knowledge_source_versions
                        WHERE source_id=%s AND valid_until IS NULL
                        ORDER BY version_number DESC LIMIT 1
                        """,
                        (source_id,),
                    )
                    version_state = cursor.fetchone()
                    old_document_managed = bool(version_state and version_state["managed"])
                    cursor.execute(
                        "UPDATE knowledge_source_versions SET valid_until=now() WHERE source_id=%s AND valid_until IS NULL",
                        (source_id,),
                    )
                    cursor.execute(
                        """
                        UPDATE knowledge_sources
                        SET source_kind=%s, authority_repository=%s, repository=%s,
                            source_path=%s, source_uri=%s, privacy_label_id=%s,
                            lifecycle_status='active', current_document_id=%s,
                            current_version=%s, current_source_revision=%s,
                            current_content_sha256=%s, last_seen_at=now(),
                            last_changed_at=now(), last_sync_run_id=%s,
                            failure_count=0, last_error=NULL, metadata=%s, updated_at=now()
                        WHERE id=%s
                        """,
                        (
                            entry["source_kind"],
                            repository,
                            repository,
                            source_path,
                            entry.get("source_uri"),
                            label_id,
                            new_document_id,
                            next_version,
                            manifest["revision"],
                            source_hash,
                            run_id,
                            Jsonb(
                                {
                                    "publisher_version": PUBLISHER_VERSION,
                                    "category": entry.get("category"),
                                    "generated": bool(entry.get("generated")),
                                    "indexed_content_sha256": indexed_hash,
                                    "title": entry.get("title"),
                                }
                            ),
                            source_id,
                        ),
                    )
                    action = "updated"
                else:
                    next_version = 1
                    cursor.execute(
                        """
                        INSERT INTO knowledge_sources (
                            source_key, source_kind, authority_repository, repository,
                            source_path, source_uri, privacy_label_id, lifecycle_status,
                            current_document_id, current_version, current_source_revision,
                            current_content_sha256, last_seen_at, last_changed_at,
                            last_sync_run_id, metadata
                        ) VALUES (
                            %s, %s, %s, %s,
                            %s, %s, %s, 'active',
                            %s, 1, %s,
                            %s, now(), now(),
                            %s, %s
                        ) RETURNING id
                        """,
                        (
                            source_key,
                            entry["source_kind"],
                            repository,
                            repository,
                            source_path,
                            entry.get("source_uri"),
                            label_id,
                            new_document_id,
                            manifest["revision"],
                            source_hash,
                            run_id,
                            Jsonb(
                                {
                                    "publisher_version": PUBLISHER_VERSION,
                                    "category": entry.get("category"),
                                    "generated": bool(entry.get("generated")),
                                    "indexed_content_sha256": indexed_hash,
                                    "title": entry.get("title"),
                                }
                            ),
                        ),
                    )
                    source_id = cursor.fetchone()["id"]
                    action = "created"

                cursor.execute(
                    """
                    INSERT INTO knowledge_source_versions (
                        source_id, version_number, document_id, source_revision,
                        content_sha256, sync_run_id, metadata
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (
                        source_id,
                        next_version,
                        new_document_id,
                        manifest["revision"],
                        source_hash,
                        run_id,
                        Jsonb(
                            {
                                "publisher_version": PUBLISHER_VERSION,
                                "indexed_content_sha256": indexed_hash,
                                "document_created_by_publisher": created_document,
                                "upload_status": upload.get("status"),
                                "chunk_count": upload.get("chunk_count"),
                                "embedding_model": upload.get("embedding_model"),
                                "encrypted_at_rest": upload.get("encrypted_at_rest"),
                                "malware_scan": upload.get("malware_scan"),
                                "redactions": entry.get("redactions", 0),
                            }
                        ),
                    ),
                )
                source_version_id = cursor.fetchone()["id"]
                cursor.execute(
                    """
                    UPDATE knowledge_source_projections SET active=false, updated_at=now()
                    WHERE source_version_id IN (
                        SELECT id FROM knowledge_source_versions
                        WHERE source_id=%s AND id<>%s
                    ) AND active=true
                    """,
                    (source_id, source_version_id),
                )

                target_id: UUID | None = None
                target_key = f"{repository}:{source_path}"
                if entry.get("category") == "repository-context":
                    target_id = upsert_repository_context(
                        cursor,
                        manifest=manifest,
                        entry=entry,
                        label_id=label_id,
                    )
                    target_key = repository
                architecture_id = upsert_architecture_record(
                    cursor,
                    manifest=manifest,
                    entry=entry,
                    label_id=label_id,
                )
                if architecture_id is not None:
                    target_id = architecture_id
                    target_key = f"github:{repository}:{source_path}"
                schema_id = upsert_schema_asset(
                    cursor,
                    manifest=manifest,
                    entry=entry,
                    label_id=label_id,
                )
                if schema_id is not None:
                    target_id = schema_id
                    target_key = f"{repository}:{source_path}"
                projected_issues = upsert_issue_steps(cursor, manifest=manifest, entry=entry)

                cursor.execute(
                    """
                    INSERT INTO knowledge_source_projections (
                        source_version_id, projection_kind, target_key, target_id,
                        extraction_method, confidence, verification_status,
                        active, payload
                    ) VALUES (%s, %s, %s, %s, 'deterministic', 1.0, 'verified', true, %s)
                    ON CONFLICT (source_version_id, projection_kind, target_key)
                    DO UPDATE SET target_id=EXCLUDED.target_id,
                                  confidence=1.0,
                                  verification_status='verified',
                                  active=true,
                                  payload=EXCLUDED.payload,
                                  updated_at=now()
                    """,
                    (
                        source_version_id,
                        projection_kind(str(entry.get("category") or "documentation")),
                        target_key,
                        target_id,
                        Jsonb(
                            {
                                "publisher_version": PUBLISHER_VERSION,
                                "repository": repository,
                                "source_path": source_path,
                                "source_uri": entry.get("source_uri"),
                                "title": entry.get("title"),
                                "summary": entry.get("summary"),
                                "category": entry.get("category"),
                                "projected_issue_count": projected_issues,
                                "records": entry.get("records") or [],
                            }
                        ),
                    ),
                )
            connection.commit()
    except Exception:
        if created_document:
            try:
                delete_document(
                    new_document_id,
                    purge_object=True,
                    reason="repository-source-ledger-transaction-failed",
                )
            except Exception:
                pass
        raise

    if old_document_id and old_document_managed and old_document_id != new_document_id:
        with psycopg.connect(database_url, row_factory=dict_row, connect_timeout=10) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT count(*)::integer AS references
                    FROM knowledge_sources
                    WHERE lifecycle_status='active' AND current_document_id=%s
                    """,
                    (old_document_id,),
                )
                references = int(cursor.fetchone()["references"])
        if references == 0:
            delete_document(
                old_document_id,
                purge_object=False,
                reason="superseded-repository-source-version",
            )
    return action, new_document_id, created_document


def reconcile_missing_sources(
    *,
    database_url: str,
    manifest: dict[str, Any],
    run_id: UUID,
    current_source_keys: set[str],
) -> int:
    repository = manifest["repository"]
    cleanups: list[tuple[str, bool]] = []
    missing = 0
    with psycopg.connect(database_url, row_factory=dict_row, connect_timeout=10) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, source_key, current_document_id
                FROM knowledge_sources
                WHERE repository=%s
                  AND lifecycle_status='active'
                  AND metadata->>'publisher_version'=%s
                FOR UPDATE
                """,
                (repository, PUBLISHER_VERSION),
            )
            for source in cursor.fetchall():
                if source["source_key"] in current_source_keys:
                    continue
                cursor.execute(
                    """
                    SELECT COALESCE((metadata->>'document_created_by_publisher')::boolean, false) AS managed
                    FROM knowledge_source_versions
                    WHERE source_id=%s AND valid_until IS NULL
                    ORDER BY version_number DESC LIMIT 1
                    """,
                    (source["id"],),
                )
                version = cursor.fetchone()
                managed = bool(version and version["managed"])
                cursor.execute(
                    "UPDATE knowledge_source_versions SET valid_until=now() WHERE source_id=%s AND valid_until IS NULL",
                    (source["id"],),
                )
                cursor.execute(
                    """
                    UPDATE knowledge_source_projections SET active=false, updated_at=now()
                    WHERE source_version_id IN (
                        SELECT id FROM knowledge_source_versions WHERE source_id=%s
                    ) AND active=true
                    """,
                    (source["id"],),
                )
                cursor.execute(
                    """
                    UPDATE knowledge_sources
                    SET lifecycle_status='missing', last_seen_at=now(),
                        last_sync_run_id=%s, updated_at=now()
                    WHERE id=%s
                    """,
                    (run_id, source["id"]),
                )
                if source["current_document_id"]:
                    cleanups.append((str(source["current_document_id"]), managed))
                missing += 1
        connection.commit()

    for document_id, managed in cleanups:
        if not managed:
            continue
        with psycopg.connect(database_url, row_factory=dict_row, connect_timeout=10) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT count(*)::integer AS references FROM knowledge_sources "
                    "WHERE lifecycle_status='active' AND current_document_id=%s",
                    (document_id,),
                )
                references = int(cursor.fetchone()["references"])
        if references == 0:
            delete_document(
                document_id,
                purge_object=False,
                reason="repository-source-missing-from-authoritative-commit",
            )
    return missing


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--run-key", required=True)
    parser.add_argument("--trigger-kind", default="reconcile")
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args()

    root = Path(args.root).resolve()
    manifest = require_manifest(root)
    manifest["trigger_kind"] = args.trigger_kind
    database_url = os.environ.get(DATABASE_URL_ENV, "")
    if not database_url:
        raise SyncError("Agent Fabric database URL is unavailable")

    counts = {
        "discovered": len(manifest["entries"]),
        "unchanged": 0,
        "created": 0,
        "updated": 0,
        "missing": 0,
        "failed": 0,
    }
    failures: list[dict[str, str]] = []
    documents: list[str] = []

    with psycopg.connect(database_url, row_factory=dict_row, connect_timeout=10) as connection:
        with connection.cursor() as cursor:
            verify_schema(cursor)
            verify_repository_scope(cursor, manifest["repository"])
        connection.commit()
        run_id = start_run(
            connection,
            run_key=args.run_key,
            repository=manifest["repository"],
            revision=manifest["revision"],
            manifest=manifest,
        )

    current_source_keys: set[str] = set()
    for entry in manifest["entries"]:
        source_key = str(entry.get("source_key") or "")
        current_source_keys.add(source_key)
        try:
            action, document_id, _ = synchronise_entry(
                database_url=database_url,
                root=root,
                manifest=manifest,
                entry=entry,
                run_id=run_id,
            )
            counts[action] += 1
            if document_id:
                documents.append(document_id)
        except Exception as exc:
            counts["failed"] += 1
            failures.append(
                {
                    "source_key": source_key,
                    "error_type": type(exc).__name__,
                    "message": str(exc)[:500],
                }
            )
            with psycopg.connect(database_url, row_factory=dict_row, connect_timeout=10) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE knowledge_sources
                        SET failure_count=failure_count+1,
                            last_error=%s,
                            last_sync_run_id=%s,
                            updated_at=now()
                        WHERE source_key=%s
                        """,
                        (f"{type(exc).__name__}: {str(exc)[:500]}", run_id, source_key),
                    )
                connection.commit()

    try:
        counts["missing"] = reconcile_missing_sources(
            database_url=database_url,
            manifest=manifest,
            run_id=run_id,
            current_source_keys=current_source_keys,
        )
    except Exception as exc:
        counts["failed"] += 1
        failures.append(
            {
                "source_key": f"repository:{manifest['repository']}:missing-reconciliation",
                "error_type": type(exc).__name__,
                "message": str(exc)[:500],
            }
        )

    run_status = "succeeded" if counts["failed"] == 0 else "partial"
    with psycopg.connect(database_url, row_factory=dict_row, connect_timeout=10) as connection:
        finish_run(
            connection,
            run_id=run_id,
            status=run_status,
            counts=counts,
            error_summary=(json.dumps(failures, ensure_ascii=False)[:8000] if failures else None),
        )

    receipt = {
        "schema_version": 1,
        "publisher_version": PUBLISHER_VERSION,
        "status": run_status,
        "repository": manifest["repository"],
        "revision": manifest["revision"],
        "visibility": manifest["visibility"],
        "privacy_label": manifest["privacy_label"],
        "run_id": str(run_id),
        "counts": counts,
        "distinct_document_count": len(set(documents)),
        "failures": failures,
        "source_text_retained": False,
        "credentials_retained": False,
        "external_embedding_model_used": False,
    }
    receipt_path = Path(args.receipt)
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(json.dumps(safe_json(receipt), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: receipt[key] for key in ("status", "repository", "revision", "counts", "distinct_document_count")}))
    return 0 if run_status == "succeeded" else 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"synchronizer_error={type(exc).__name__}: {str(exc)[:1000]}", file=sys.stderr)
        raise
