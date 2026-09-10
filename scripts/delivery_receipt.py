#!/usr/bin/env python3
"""Create and validate minimal, secret-safe asynchronous delivery receipts."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
import time
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlsplit


SCHEMA = "delivery.receipt.v1"
PROVIDERS = {
    "apple",
    "aws",
    "chrome-web-store",
    "cloudflare",
    "google-play",
    "linkedin",
    "microsoft-store",
    "web",
    "x",
    "youtube",
}
EFFECTS = {"prepare", "stage", "submit", "release", "verify"}
MATERIAL_EFFECTS = {"stage", "submit", "release", "verify"}
LEGACY_CONSEQUENTIAL_EFFECTS = {"submit", "release", "verify"}
PHASES = {
    "observed",
    "prepared",
    "uploaded",
    "processing",
    "staged",
    "submitted",
    "in_review",
    "approved",
    "scheduled",
    "released",
    "verified",
    "rejected",
    "failed",
    "blocked",
    "effect_unknown",
}

SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:@/+\-]{0,255}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
SECRET_ASSIGNMENT = re.compile(
    r"(?i)\b(?:api[_-]?key|client[_-]?secret|access[_-]?token|refresh[_-]?token|"
    r"token|cookie|secret|private[_-]?key|password|passphrase|authorization|"
    r"session[_-]?uri|upload[_-]?uri|upload[_-]?id|recovery[_-]?code)\b"
    r"[\"']?\s*[:=]"
)
JWT = re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\b")
AUTH_HEADER = re.compile(r"(?i)\b(?:Bearer|Basic)\s+[A-Za-z0-9._~+/=-]{8,}")
KNOWN_TOKEN = re.compile(
    r"(?:\bAIza[0-9A-Za-z_-]{30,}\b|\bgh[pousr]_[0-9A-Za-z]{20,}\b)"
)
SENSITIVE_QUERY_KEYS = {
    "access_token",
    "api_key",
    "auth",
    "authorization",
    "client_secret",
    "code",
    "cookie",
    "credential",
    "key",
    "password",
    "refresh_token",
    "secret",
    "session",
    "signature",
    "sig",
    "token",
    "upload_id",
    "x-amz-credential",
    "x-amz-signature",
    "x-goog-credential",
    "x-goog-signature",
}


class ReceiptError(ValueError):
    """A safe, user-correctable receipt error."""


class JsonArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise ReceiptError("invalid command arguments; use --help")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _parse_time(value: str, field: str) -> str:
    _safe_text(field, value, maximum=64)
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ReceiptError(f"{field} must be an ISO-8601 timestamp") from exc
    if parsed.tzinfo is None:
        raise ReceiptError(f"{field} must include a timezone")
    try:
        parsed.astimezone(timezone.utc)
    except (ValueError, OverflowError) as exc:
        raise ReceiptError(f"{field} is outside the supported UTC range") from exc
    return value


def _safe_text(field: str, value: str, *, maximum: int = 512) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ReceiptError(f"{field} must be a non-empty string")
    if len(value) > maximum:
        raise ReceiptError(f"{field} exceeds {maximum} characters")
    if "\n" in value or "\r" in value or "\x00" in value:
        raise ReceiptError(f"{field} contains unsupported control characters")
    if (
        "-----BEGIN" in value.upper()
        or "op://" in value.lower()
        or SECRET_ASSIGNMENT.search(value)
        or JWT.search(value)
        or AUTH_HEADER.search(value)
        or KNOWN_TOKEN.search(value)
    ):
        raise ReceiptError(f"{field} appears to contain protected material")

    candidate = value
    if "://" in candidate:
        try:
            parsed = urlsplit(candidate)
        except ValueError as exc:
            raise ReceiptError(f"{field} contains an invalid URL") from exc
        if parsed.username is not None or parsed.password is not None:
            raise ReceiptError(f"{field} appears to contain URL userinfo")
        for component in (parsed.query, parsed.fragment):
            for key, _ in parse_qsl(component, keep_blank_values=True):
                if _sensitive_query_key(key):
                    raise ReceiptError(f"{field} appears to contain a signed or secret URL")
    elif "?" in candidate or "#" in candidate:
        query = candidate.split("?", 1)[1] if "?" in candidate else ""
        fragment = candidate.split("#", 1)[1] if "#" in candidate else ""
        for component in (query.split("#", 1)[0], fragment):
            for key, _ in parse_qsl(component, keep_blank_values=True):
                if _sensitive_query_key(key):
                    raise ReceiptError(f"{field} appears to contain a signed or secret URL")
    return value


def _sensitive_query_key(key: str) -> bool:
    normalized = key.lower()
    return (
        normalized in SENSITIVE_QUERY_KEYS
        or normalized.startswith("x-amz-")
        or normalized.startswith("x-goog-")
    )


def _lock_path(receipt_path: Path) -> Path:
    normalized = os.path.normcase(os.path.abspath(receipt_path))
    identity = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
    return Path(tempfile.gettempdir()) / "delivery-receipt-locks" / f"{identity}.lock"


@contextmanager
def _exclusive_lock(receipt_path: Path):
    lock_path = _lock_path(receipt_path)
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+b") as stream:
        stream.seek(0, os.SEEK_END)
        if stream.tell() == 0:
            stream.write(b"\0")
            stream.flush()
        stream.seek(0)
        try:
            if os.name == "nt":
                import msvcrt

                msvcrt.locking(stream.fileno(), msvcrt.LK_LOCK, 1)
            else:
                import fcntl

                fcntl.flock(stream.fileno(), fcntl.LOCK_EX)
        except OSError as exc:
            raise ReceiptError("receipt is busy; retry after the current operation finishes") from exc
        try:
            yield
        finally:
            try:
                stream.seek(0)
                if os.name == "nt":
                    import msvcrt

                    msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
                else:
                    import fcntl

                    fcntl.flock(stream.fileno(), fcntl.LOCK_UN)
            except OSError:
                pass


def _safe_id(field: str, value: str) -> str:
    _safe_text(field, value, maximum=256)
    if not SAFE_ID.fullmatch(value):
        raise ReceiptError(f"{field} contains unsupported characters")
    return value


def _digest(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ReceiptError("artifact or metadata path is not a regular file")
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
            size += len(chunk)
    _safe_text("artifact name", path.name, maximum=255)
    return {"name": path.name, "sha256": digest.hexdigest(), "size": size}


def _json_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def _invalid_constant(_value: str) -> None:
    raise ValueError("non-finite JSON number")


def _load(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_json_object,
            parse_constant=_invalid_constant,
        )
    except FileNotFoundError as exc:
        raise ReceiptError("receipt file does not exist") from exc
    except (OSError, ValueError, RecursionError) as exc:
        raise ReceiptError("receipt file is unreadable or invalid JSON") from exc
    if not isinstance(data, dict):
        raise ReceiptError("receipt root must be an object")
    return data


def _write(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    temporary_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            newline="\n",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as stream:
            temporary_name = stream.name
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        for attempt in range(5):
            try:
                os.replace(temporary_name, path)
                break
            except PermissionError:
                if os.name != "nt" or attempt == 4:
                    raise
                time.sleep(0.05 * (2**attempt))
        temporary_name = None
        try:
            os.chmod(path, 0o600)
        except OSError:
            pass
    finally:
        if temporary_name:
            try:
                Path(temporary_name).unlink()
            except OSError:
                pass


def _validate_blob(field: str, value: Any) -> None:
    if not isinstance(value, dict):
        raise ReceiptError(f"{field} must be an object")
    if set(value) != {"name", "sha256", "size"}:
        raise ReceiptError(f"{field} has unexpected fields")
    _safe_text(f"{field}.name", value["name"], maximum=255)
    if not isinstance(value["sha256"], str) or not SHA256.fullmatch(value["sha256"]):
        raise ReceiptError(f"{field}.sha256 must be lowercase SHA-256")
    if isinstance(value["size"], bool) or not isinstance(value["size"], int) or value["size"] < 0:
        raise ReceiptError(f"{field}.size must be a non-negative integer")


def validate_receipt(data: dict[str, Any]) -> None:
    required = {
        "schema",
        "delivery_id",
        "provider",
        "provider_account_id",
        "release_id",
        "target",
        "intent",
        "artifact",
        "created_at",
        "events",
    }
    allowed = required | {"metadata"}
    missing = required - set(data)
    unexpected = set(data) - allowed
    if missing:
        raise ReceiptError(f"receipt is missing fields: {', '.join(sorted(missing))}")
    if unexpected:
        raise ReceiptError("receipt has unexpected fields")
    if data["schema"] != SCHEMA:
        raise ReceiptError("unsupported receipt schema")
    _safe_id("delivery_id", data["delivery_id"])
    if not isinstance(data["provider"], str) or data["provider"] not in PROVIDERS:
        raise ReceiptError("provider is unsupported")
    _safe_id("provider_account_id", data["provider_account_id"])
    _safe_id("release_id", data["release_id"])

    target = data["target"]
    if not isinstance(target, dict) or set(target) != {"kind", "id"}:
        raise ReceiptError("target must contain exactly kind and id")
    _safe_id("target.kind", target["kind"])
    _safe_id("target.id", target["id"])

    intent = data["intent"]
    if not isinstance(intent, dict) or set(intent) != {"channel", "effect", "release_mode"}:
        raise ReceiptError("intent must contain exactly channel, effect, and release_mode")
    _safe_id("intent.channel", intent["channel"])
    if not isinstance(intent["effect"], str) or intent["effect"] not in EFFECTS:
        raise ReceiptError("intent.effect is unsupported")
    _safe_id("intent.release_mode", intent["release_mode"])
    if intent["effect"] in LEGACY_CONSEQUENTIAL_EFFECTS and "metadata" not in data:
        raise ReceiptError("consequential effects require a bound metadata manifest")

    _validate_blob("artifact", data["artifact"])
    if "metadata" in data:
        _validate_blob("metadata", data["metadata"])
    _parse_time(data["created_at"], "created_at")

    events = data["events"]
    if not isinstance(events, list):
        raise ReceiptError("events must be an array")
    seen: set[str] = set()
    allowed_event = {
        "id",
        "phase",
        "observed_at",
        "status",
        "provider_object_kind",
        "provider_object_id",
        "evidence_ref",
        "next_action",
    }
    required_event = {"id", "phase", "observed_at", "status"}
    for event in events:
        if not isinstance(event, dict):
            raise ReceiptError("event must be an object")
        if required_event - set(event) or set(event) - allowed_event:
            raise ReceiptError("event fields are missing or unexpected")
        event_id = _safe_id("event.id", event["id"])
        if event_id in seen:
            raise ReceiptError("event IDs must be unique")
        seen.add(event_id)
        if not isinstance(event["phase"], str) or event["phase"] not in PHASES:
            raise ReceiptError("event phase is unsupported")
        _parse_time(event["observed_at"], "event.observed_at")
        _safe_text("event.status", event["status"])
        has_object_kind = "provider_object_kind" in event
        has_object_id = "provider_object_id" in event
        if has_object_kind and not has_object_id:
            raise ReceiptError(
                "event provider_object_kind requires provider_object_id"
            )
        if has_object_kind:
            _safe_id("event.provider_object_kind", event["provider_object_kind"])
            _safe_id("event.provider_object_id", event["provider_object_id"])
        elif has_object_id:
            # v0.1 receipts had an untyped provider_object_id. Keep them
            # readable, while command_record requires typed IDs for new events.
            _safe_text("event.provider_object_id", event["provider_object_id"])
        for field in ("evidence_ref", "next_action"):
            if field in event:
                _safe_text(f"event.{field}", event[field])

    provider_objects: dict[str, str] = {}
    for event in events:
        if "provider_object_kind" not in event:
            continue
        kind = event["provider_object_kind"]
        object_id = event["provider_object_id"]
        previous = provider_objects.setdefault(kind, object_id)
        if previous != object_id:
            raise ReceiptError(
                "provider object kind maps to more than one ID in this delivery epoch"
            )


def _epoch(data: dict[str, Any]) -> dict[str, Any]:
    return {
        key: data[key]
        for key in (
            "schema",
            "delivery_id",
            "provider",
            "provider_account_id",
            "release_id",
            "target",
            "intent",
            "artifact",
            "metadata",
        )
        if key in data
    }


def command_init(args: argparse.Namespace) -> dict[str, Any]:
    path = Path(args.file)
    with _exclusive_lock(path):
        if args.effect in MATERIAL_EFFECTS and not args.metadata_file:
            raise ReceiptError(
                "stage and later effects require a bound metadata manifest"
            )
        created_at = _parse_time(args.created_at or _now(), "created_at")
        receipt: dict[str, Any] = {
            "schema": SCHEMA,
            "delivery_id": _safe_id("delivery_id", args.delivery_id),
            "provider": args.provider,
            "provider_account_id": _safe_id(
                "provider_account_id", args.provider_account_id
            ),
            "release_id": _safe_id("release_id", args.release_id),
            "target": {
                "kind": _safe_id("target.kind", args.target_kind),
                "id": _safe_id("target.id", args.target_id),
            },
            "intent": {
                "channel": _safe_id("intent.channel", args.channel),
                "effect": args.effect,
                "release_mode": _safe_id("intent.release_mode", args.release_mode),
            },
            "artifact": _digest(Path(args.artifact)),
            "created_at": created_at,
            "events": [],
        }
        if args.metadata_file:
            receipt["metadata"] = _digest(Path(args.metadata_file))
        validate_receipt(receipt)

        if path.exists():
            existing = _load(path)
            validate_receipt(existing)
            if _epoch(existing) != _epoch(receipt):
                raise ReceiptError("existing receipt belongs to a different delivery epoch")
            return {
                "ok": True,
                "operation": "init",
                "status": "already_exists",
                "receipt": existing,
            }

        _write(path, receipt)
        return {
            "ok": True,
            "operation": "init",
            "status": "created",
            "receipt": receipt,
        }


def _optional_event_field(event: dict[str, Any], field: str, value: str | None) -> None:
    if value is not None:
        event[field] = _safe_text(f"event.{field}", value)


def command_record(args: argparse.Namespace) -> dict[str, Any]:
    path = Path(args.file)
    with _exclusive_lock(path):
        receipt = _load(path)
        validate_receipt(receipt)
        if bool(args.provider_object_kind) != bool(args.provider_object_id):
            raise ReceiptError(
                "new provider objects require both --provider-object-kind and --provider-object-id"
            )
        event_id = _safe_id("event.id", args.event_id)
        existing = next(
            (event for event in receipt["events"] if event["id"] == event_id),
            None,
        )
        observed_at = args.observed_at or (existing and existing["observed_at"]) or _now()
        event: dict[str, Any] = {
            "id": event_id,
            "phase": args.phase,
            "observed_at": _parse_time(observed_at, "event.observed_at"),
            "status": _safe_text("event.status", args.status),
        }
        _optional_event_field(
            event, "provider_object_kind", args.provider_object_kind
        )
        _optional_event_field(event, "provider_object_id", args.provider_object_id)
        _optional_event_field(event, "evidence_ref", args.evidence_ref)
        _optional_event_field(event, "next_action", args.next_action)

        if existing is not None:
            if existing != event:
                raise ReceiptError("event ID already exists with different content")
            return {
                "ok": True,
                "operation": "record",
                "status": "already_recorded",
                "event": existing,
            }

        receipt["events"].append(event)
        validate_receipt(receipt)
        _write(path, receipt)
        return {
            "ok": True,
            "operation": "record",
            "status": "recorded",
            "event": event,
        }


def command_validate(args: argparse.Namespace) -> dict[str, Any]:
    path = Path(args.file)
    with _exclusive_lock(path):
        receipt = _load(path)
        validate_receipt(receipt)
        checks: dict[str, str] = {"schema": "valid"}
        if args.artifact:
            actual = _digest(Path(args.artifact))
            if actual != receipt["artifact"]:
                raise ReceiptError(
                    "artifact does not match the bound name, size, and SHA-256"
                )
            checks["artifact"] = "matches"
        else:
            checks["artifact"] = "not_checked"

        if "metadata" in receipt and not args.metadata_file:
            raise ReceiptError("receipt binds metadata; --metadata-file is required")
        legacy_missing_metadata = (
            receipt["intent"]["effect"] in MATERIAL_EFFECTS
            and "metadata" not in receipt
        )
        if legacy_missing_metadata:
            checks["metadata"] = "legacy_missing"
        if args.metadata_file:
            if "metadata" not in receipt:
                raise ReceiptError("receipt has no bound metadata file")
            actual_metadata = _digest(Path(args.metadata_file))
            if actual_metadata != receipt["metadata"]:
                raise ReceiptError(
                    "metadata does not match the bound name, size, and SHA-256"
                )
            checks["metadata"] = "matches"

        complete = args.artifact is not None and not legacy_missing_metadata
        return {
            "ok": True,
            "operation": "validate",
            "status": (
                "valid"
                if complete
                else "incomplete"
                if args.artifact is not None
                else "schema_valid"
            ),
            "complete": complete,
            "checks": checks,
            "latest_event": max(
                receipt["events"],
                key=lambda event: (
                    datetime.fromisoformat(
                        event["observed_at"].replace("Z", "+00:00")
                    ).astimezone(timezone.utc),
                    event["id"],
                ),
            )
            if receipt["events"]
            else None,
        }


def command_show(args: argparse.Namespace) -> dict[str, Any]:
    path = Path(args.file)
    with _exclusive_lock(path):
        receipt = _load(path)
        validate_receipt(receipt)
        return {"ok": True, "operation": "show", "receipt": receipt}


def build_parser() -> argparse.ArgumentParser:
    parser = JsonArgumentParser(
        description="Create and validate minimal delivery receipts. JSON is always written to stdout."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init = subparsers.add_parser("init", help="Create an artifact-bound receipt")
    init.add_argument("--file", required=True)
    init.add_argument("--delivery-id", required=True)
    init.add_argument("--provider", choices=sorted(PROVIDERS), required=True)
    init.add_argument("--provider-account-id", required=True)
    init.add_argument("--release-id", required=True)
    init.add_argument("--target-kind", required=True)
    init.add_argument("--target-id", required=True)
    init.add_argument("--channel", required=True)
    init.add_argument("--effect", choices=sorted(EFFECTS), required=True)
    init.add_argument("--release-mode", required=True)
    init.add_argument("--artifact", required=True)
    init.add_argument("--metadata-file")
    init.add_argument("--created-at")
    init.set_defaults(handler=command_init)

    record = subparsers.add_parser("record", help="Append one idempotent observed event")
    record.add_argument("--file", required=True)
    record.add_argument("--event-id", required=True)
    record.add_argument("--phase", choices=sorted(PHASES), required=True)
    record.add_argument("--observed-at")
    record.add_argument("--status", required=True)
    record.add_argument("--provider-object-kind")
    record.add_argument("--provider-object-id")
    record.add_argument("--evidence-ref")
    record.add_argument("--next-action")
    record.set_defaults(handler=command_record)

    validate = subparsers.add_parser("validate", help="Validate receipt and optional bound files")
    validate.add_argument("--file", required=True)
    validate.add_argument("--artifact")
    validate.add_argument("--metadata-file")
    validate.set_defaults(handler=command_validate)

    show = subparsers.add_parser("show", help="Return a validated receipt")
    show.add_argument("--file", required=True)
    show.set_defaults(handler=command_show)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
        result = args.handler(args)
    except ReceiptError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=True))
        return 2
    except OSError:
        print(
            json.dumps(
                {"ok": False, "error": "receipt filesystem operation failed"},
                ensure_ascii=True,
            )
        )
        return 2
    print(json.dumps(result, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
