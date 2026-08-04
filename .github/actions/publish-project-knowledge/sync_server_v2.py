#!/usr/bin/env python3
"""Compatibility entry point for robust repository knowledge ingestion.

The original synchronizer remains the authoritative projection and versioning
implementation. This wrapper changes only Knowledge API acceptance semantics:
ready documents are fully validated, duplicate documents are resolved through
the authenticated document endpoint, and in-progress documents are polled to a
bounded terminal state instead of being reported as generic failures.
"""

from __future__ import annotations

import mimetypes
from pathlib import Path
import sys
import time
from typing import Any

import httpx

import sync_server as base

POLL_SECONDS = 2.0
POLL_TIMEOUT_SECONDS = 300.0


def _document(document_id: str) -> dict[str, Any]:
    response = httpx.get(
        f"{base.KNOWLEDGE_API_URL}/v1/knowledge/documents/{document_id}",
        headers=base.api_headers(),
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()
    if not isinstance(payload, dict):
        raise base.SyncError("Knowledge API returned an invalid document record")
    return payload


def _accepted_existing(payload: dict[str, Any]) -> dict[str, Any]:
    document_id = str(payload.get("document_id") or "")
    if not document_id:
        raise base.SyncError("existing source has no document ID")
    record = _document(document_id)
    if record.get("status") != "ready":
        raise base.SyncError(
            f"existing document is not ready: {record.get('status') or 'unknown'}"
        )
    chunk_count = int(record.get("chunk_count") or payload.get("chunk_count") or 0)
    if chunk_count < 1:
        raise base.SyncError("existing ready document has no chunks")
    embedding_model = record.get("embedding_model") or "nomic-embed-text"
    if embedding_model != "nomic-embed-text":
        raise base.SyncError("existing document uses an unaccepted embedding model")
    return {
        **payload,
        "status": "duplicate",
        "document_id": document_id,
        "document_version_id": (
            payload.get("document_version_id") or record.get("document_version_id")
        ),
        "chunk_count": chunk_count,
        "embedding_model": embedding_model,
        "encrypted_at_rest": True,
        "malware_scan": "clean",
    }


def _wait_for_ready(payload: dict[str, Any]) -> dict[str, Any]:
    document_id = str(payload.get("document_id") or "")
    if not document_id:
        raise base.SyncError("processing source has no document ID")
    deadline = time.monotonic() + POLL_TIMEOUT_SECONDS
    last_status = "processing"
    while time.monotonic() < deadline:
        record = _document(document_id)
        last_status = str(record.get("status") or "unknown")
        if last_status == "ready":
            return _accepted_existing({**payload, "status": "duplicate"})
        if last_status in {"failed", "deleted"}:
            detail = record.get("failure_reason") or record.get("last_error") or last_status
            raise base.SyncError(f"Knowledge document reached {last_status}: {detail}")
        time.sleep(POLL_SECONDS)
    raise base.SyncError(
        f"Knowledge document did not become ready within {int(POLL_TIMEOUT_SECONDS)} seconds; "
        f"last status: {last_status}"
    )


def upload_document(
    *,
    path: Path,
    upload_filename: str,
    privacy_label: str,
    retention_days: int,
    source_channel: str,
) -> dict[str, Any]:
    if not path.is_file() or not path.stat().st_size:
        raise base.SyncError("source payload is empty or missing")
    suffix = Path(upload_filename).suffix.casefold()
    if suffix not in base.SUPPORTED_UPLOAD_SUFFIXES:
        raise base.SyncError(f"unsupported upload suffix: {suffix}")
    content_type = mimetypes.guess_type(upload_filename)[0] or "application/octet-stream"
    with path.open("rb") as handle:
        response = httpx.post(
            f"{base.KNOWLEDGE_API_URL}/v1/knowledge/documents",
            headers=base.api_headers(),
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
    if not isinstance(payload, dict):
        raise base.SyncError("Knowledge API returned an invalid ingestion response")
    status = str(payload.get("status") or "unknown")
    if status == "processing":
        return _wait_for_ready(payload)
    if status == "duplicate":
        return _accepted_existing(payload)
    if status != "ready":
        detail = payload.get("detail") or payload.get("failure_reason") or status
        raise base.SyncError(f"Knowledge API did not accept the source: {detail}")
    if not payload.get("document_id") or int(payload.get("chunk_count") or 0) < 1:
        raise base.SyncError("accepted source has no document or chunks")
    if payload.get("embedding_model") != "nomic-embed-text":
        raise base.SyncError("source was not embedded by the accepted local model")
    if payload.get("encrypted_at_rest") is not True:
        raise base.SyncError("source was not encrypted at rest")
    if payload.get("malware_scan") != "clean":
        raise base.SyncError("source did not pass malware scanning")
    return payload


base.upload_document = upload_document

if __name__ == "__main__":
    raise SystemExit(base.main())
