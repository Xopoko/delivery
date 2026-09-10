from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = PLUGIN_ROOT / "scripts" / "delivery_receipt.py"


class DeliveryReceiptTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.artifact = self.root / "release.bin"
        self.artifact.write_bytes(b"exact release bytes\n")
        self.metadata = self.root / "release-intent.json"
        self.metadata.write_text(
            '{"audience":"private","notify":false}\n', encoding="utf-8"
        )
        self.receipt = self.root / "receipt.json"

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def run_cli(
        self,
        *arguments: str,
        expected_code: int = 0,
        environment: dict[str, str] | None = None,
    ) -> dict:
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), *arguments],
            text=True,
            capture_output=True,
            check=False,
            env=environment,
        )
        self.assertEqual(completed.returncode, expected_code, completed.stderr)
        self.assertEqual(completed.stderr, "")
        return json.loads(completed.stdout)

    def init_receipt(self) -> dict:
        return self.run_cli(
            "init",
            "--file",
            str(self.receipt),
            "--delivery-id",
            "release-7",
            "--provider",
            "youtube",
            "--provider-account-id",
            "UCexample",
            "--release-id",
            "short-7",
            "--target-kind",
            "video",
            "--target-id",
            "planned-short-7",
            "--channel",
            "private",
            "--effect",
            "stage",
            "--release-mode",
            "private",
            "--artifact",
            str(self.artifact),
            "--metadata-file",
            str(self.metadata),
            "--created-at",
            "2026-08-24T12:00:00Z",
        )

    def test_init_is_idempotent_and_validate_detects_artifact_change(self) -> None:
        created = self.init_receipt()
        self.assertEqual(created["status"], "created")
        self.assertEqual(created["receipt"]["artifact"]["name"], "release.bin")
        self.assertNotIn(str(self.root), json.dumps(created))

        repeated = self.init_receipt()
        self.assertEqual(repeated["status"], "already_exists")

        valid = self.run_cli(
            "validate",
            "--file",
            str(self.receipt),
            "--artifact",
            str(self.artifact),
            "--metadata-file",
            str(self.metadata),
        )
        self.assertEqual(valid["checks"]["artifact"], "matches")

        self.artifact.write_bytes(b"changed bytes\n")
        mismatch = self.run_cli(
            "validate",
            "--file",
            str(self.receipt),
            "--artifact",
            str(self.artifact),
            expected_code=2,
        )
        self.assertFalse(mismatch["ok"])
        self.assertIn("does not match", mismatch["error"])

    def test_event_id_is_idempotent_but_conflicting_reuse_fails(self) -> None:
        self.init_receipt()
        arguments = (
            "record",
            "--file",
            str(self.receipt),
            "--event-id",
            "upload-1",
            "--phase",
            "uploaded",
            "--observed-at",
            "2026-08-24T12:05:00Z",
            "--status",
            "provider accepted bytes",
            "--provider-object-id",
            "video-42",
            "--provider-object-kind",
            "video",
            "--evidence-ref",
            "api:videos.insert",
            "--next-action",
            "observe processing",
        )
        first = self.run_cli(*arguments)
        self.assertEqual(first["status"], "recorded")
        second = self.run_cli(*arguments)
        self.assertEqual(second["status"], "already_recorded")

        conflict = self.run_cli(
            "record",
            "--file",
            str(self.receipt),
            "--event-id",
            "upload-1",
            "--phase",
            "failed",
            "--observed-at",
            "2026-08-24T12:05:00Z",
            "--status",
            "different outcome",
            expected_code=2,
        )
        self.assertIn("different content", conflict["error"])

    def test_secret_shaped_event_is_rejected_without_echoing_value(self) -> None:
        self.init_receipt()
        protected_values = (
            "Authorization: Bearer abcdefghijklmnopqrstuvwxyz",
            "token=abcdefghijklmnopqrstuvwxyz",
            '"api_key":"abcdefghijklmnopqrstuvwxyz"',
            "Cookie=abcdefghijklmnopqrstuvwxyz",
            "secret=abcdefghijklmnopqrstuvwxyz",
            "OP://private-vault/item/token",
            "https://user:password@example.com/private",
            "https://example.com/upload?upload_id=abcdefghijklmnopqrstuvwxyz",
            "https://example.com/callback#token=abcdefghijklmnopqrstuvwxyz",
            "https://example.com/object?X-Goog-Signature=abcdef",
        )
        for index, protected_value in enumerate(protected_values):
            with self.subTest(protected_value=protected_value.split("=", 1)[0]):
                result = self.run_cli(
                    "record",
                    "--file",
                    str(self.receipt),
                    "--event-id",
                    f"unsafe-{index}",
                    "--phase",
                    "blocked",
                    "--observed-at",
                    "2026-08-24T12:10:00Z",
                    "--status",
                    protected_value,
                    expected_code=2,
                )
                self.assertFalse(result["ok"])
                self.assertNotIn(protected_value, json.dumps(result))

        shown = self.run_cli("show", "--file", str(self.receipt))
        self.assertEqual(shown["receipt"]["events"], [])

    def test_metadata_manifest_can_be_bound_and_revalidated(self) -> None:
        metadata = self.root / "release-metadata.json"
        metadata.write_text('{"title":"Exact release"}\n', encoding="utf-8")
        created = self.run_cli(
            "init",
            "--file",
            str(self.receipt),
            "--delivery-id",
            "play-release-2",
            "--provider",
            "google-play",
            "--provider-account-id",
            "developer-123",
            "--release-id",
            "versionCode-2",
            "--target-kind",
            "package",
            "--target-id",
            "example.app",
            "--channel",
            "internal",
            "--effect",
            "stage",
            "--release-mode",
            "internal",
            "--artifact",
            str(self.artifact),
            "--metadata-file",
            str(metadata),
            "--created-at",
            "2026-08-24T12:00:00+00:00",
        )
        self.assertEqual(created["receipt"]["metadata"]["name"], metadata.name)

        valid = self.run_cli(
            "validate",
            "--file",
            str(self.receipt),
            "--artifact",
            str(self.artifact),
            "--metadata-file",
            str(metadata),
        )
        self.assertTrue(valid["complete"])
        self.assertEqual(
            valid["checks"],
            {"schema": "valid", "artifact": "matches", "metadata": "matches"},
        )

        missing_metadata = self.run_cli(
            "validate",
            "--file",
            str(self.receipt),
            "--artifact",
            str(self.artifact),
            expected_code=2,
        )
        self.assertIn("--metadata-file is required", missing_metadata["error"])

        metadata.write_text('{"title":"Changed release"}\n', encoding="utf-8")
        mismatch = self.run_cli(
            "validate",
            "--file",
            str(self.receipt),
            "--artifact",
            str(self.artifact),
            "--metadata-file",
            str(metadata),
            expected_code=2,
        )
        self.assertIn("metadata does not match", mismatch["error"])

    def test_prepare_and_verify_effects_preserve_normalized_intent(self) -> None:
        prepared_path = self.root / "prepare.json"
        prepared = self.run_cli(
            "init",
            "--file",
            str(prepared_path),
            "--delivery-id",
            "apple-prepare-1",
            "--provider",
            "apple",
            "--provider-account-id",
            "TEAM123",
            "--release-id",
            "1.0.0+7",
            "--target-kind",
            "app",
            "--target-id",
            "123456789",
            "--channel",
            "ios-app-store",
            "--effect",
            "prepare",
            "--release-mode",
            "manual",
            "--artifact",
            str(self.artifact),
            "--created-at",
            "2026-08-24T12:00:00Z",
        )
        self.assertEqual(prepared["receipt"]["intent"]["effect"], "prepare")

        verify_path = self.root / "verify.json"
        missing_manifest = self.run_cli(
            "init",
            "--file",
            str(verify_path),
            "--delivery-id",
            "apple-verify-1",
            "--provider",
            "apple",
            "--provider-account-id",
            "TEAM123",
            "--release-id",
            "1.0.0+7",
            "--target-kind",
            "app",
            "--target-id",
            "123456789",
            "--channel",
            "ios-app-store",
            "--effect",
            "verify",
            "--release-mode",
            "manual",
            "--artifact",
            str(self.artifact),
            "--created-at",
            "2026-08-24T12:00:00Z",
            expected_code=2,
        )
        self.assertIn("metadata manifest", missing_manifest["error"])

        metadata = self.root / "apple-intent.json"
        metadata.write_text('{"territories":["PL"],"releaseMode":"manual"}\n', encoding="utf-8")
        verified = self.run_cli(
            "init",
            "--file",
            str(verify_path),
            "--delivery-id",
            "apple-verify-1",
            "--provider",
            "apple",
            "--provider-account-id",
            "TEAM123",
            "--release-id",
            "1.0.0+7",
            "--target-kind",
            "app",
            "--target-id",
            "123456789",
            "--channel",
            "ios-app-store",
            "--effect",
            "verify",
            "--release-mode",
            "manual",
            "--artifact",
            str(self.artifact),
            "--metadata-file",
            str(metadata),
            "--created-at",
            "2026-08-24T12:00:00Z",
        )
        self.assertEqual(verified["receipt"]["intent"]["effect"], "verify")

    def test_stage_requires_metadata_and_provider_objects_are_stable_by_kind(self) -> None:
        missing_metadata_path = self.root / "missing-metadata.json"
        missing_metadata = self.run_cli(
            "init",
            "--file",
            str(missing_metadata_path),
            "--delivery-id",
            "chrome-stage-1",
            "--provider",
            "chrome-web-store",
            "--provider-account-id",
            "publisher-1",
            "--release-id",
            "1.2.0",
            "--target-kind",
            "extension",
            "--target-id",
            "abcdefghijklmnop",
            "--channel",
            "trusted-testers",
            "--effect",
            "stage",
            "--release-mode",
            "staged",
            "--artifact",
            str(self.artifact),
            expected_code=2,
        )
        self.assertIn("metadata manifest", missing_metadata["error"])

        legacy_path = self.root / "legacy-stage.json"
        self.run_cli(
            "init",
            "--file",
            str(legacy_path),
            "--delivery-id",
            "legacy-stage-1",
            "--provider",
            "youtube",
            "--provider-account-id",
            "UCexample",
            "--release-id",
            "legacy-video",
            "--target-kind",
            "video",
            "--target-id",
            "planned-legacy",
            "--channel",
            "private",
            "--effect",
            "prepare",
            "--release-mode",
            "private",
            "--artifact",
            str(self.artifact),
            "--created-at",
            "2026-08-24T12:00:00Z",
        )
        legacy_receipt = json.loads(legacy_path.read_text(encoding="utf-8"))
        legacy_receipt["intent"]["effect"] = "stage"
        legacy_path.write_text(json.dumps(legacy_receipt), encoding="utf-8")
        legacy_validation = self.run_cli(
            "validate",
            "--file",
            str(legacy_path),
            "--artifact",
            str(self.artifact),
        )
        self.assertFalse(legacy_validation["complete"])
        self.assertEqual(
            legacy_validation["checks"]["metadata"], "legacy_missing"
        )

        self.init_receipt()
        self.run_cli(
            "record",
            "--file",
            str(self.receipt),
            "--event-id",
            "video-bound",
            "--phase",
            "uploaded",
            "--observed-at",
            "2026-08-24T12:30:00Z",
            "--status",
            "private upload exists",
            "--provider-object-kind",
            "video",
            "--provider-object-id",
            "video-42",
        )
        conflicting = self.run_cli(
            "record",
            "--file",
            str(self.receipt),
            "--event-id",
            "video-conflict",
            "--phase",
            "processing",
            "--observed-at",
            "2026-08-24T12:31:00Z",
            "--status",
            "different object appeared",
            "--provider-object-kind",
            "video",
            "--provider-object-id",
            "video-99",
            expected_code=2,
        )
        self.assertIn("more than one ID", conflicting["error"])

    def test_latest_event_uses_observation_time_not_append_order(self) -> None:
        self.init_receipt()
        for event_id, observed_at in (
            ("newer", "2026-08-24T12:40:00Z"),
            ("older-appended-last", "2026-08-24T12:35:00Z"),
        ):
            self.run_cli(
                "record",
                "--file",
                str(self.receipt),
                "--event-id",
                event_id,
                "--phase",
                "processing",
                "--observed-at",
                observed_at,
                "--status",
                event_id,
            )
        validated = self.run_cli(
            "validate",
            "--file",
            str(self.receipt),
            "--artifact",
            str(self.artifact),
            "--metadata-file",
            str(self.metadata),
        )
        self.assertEqual(validated["latest_event"]["id"], "newer")

    def test_unicode_output_remains_machine_readable_on_legacy_windows_encoding(self) -> None:
        self.init_receipt()
        environment = os.environ.copy()
        environment["PYTHONIOENCODING"] = "cp1251"
        result = self.run_cli(
            "record",
            "--file",
            str(self.receipt),
            "--event-id",
            "unicode-1",
            "--phase",
            "processing",
            "--observed-at",
            "2026-08-24T12:15:00Z",
            "--status",
            "processing 🚀",
            environment=environment,
        )
        self.assertEqual(result["event"]["status"], "processing 🚀")

    def test_parallel_records_do_not_lose_events(self) -> None:
        self.init_receipt()
        processes: list[subprocess.Popen[str]] = []
        for index in range(10):
            processes.append(
                subprocess.Popen(
                    [
                        sys.executable,
                        str(SCRIPT),
                        "record",
                        "--file",
                        str(self.receipt),
                        "--event-id",
                        f"parallel-{index}",
                        "--phase",
                        "processing",
                        "--observed-at",
                        f"2026-08-24T12:20:{index:02d}Z",
                        "--status",
                        f"provider observation {index}",
                    ],
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
            )

        for process in processes:
            stdout, stderr = process.communicate(timeout=20)
            self.assertEqual(process.returncode, 0, stderr)
            self.assertEqual(stderr, "")
            self.assertTrue(json.loads(stdout)["ok"])

        shown = self.run_cli("show", "--file", str(self.receipt))
        event_ids = {event["id"] for event in shown["receipt"]["events"]}
        self.assertEqual(event_ids, {f"parallel-{index}" for index in range(10)})

    def test_malformed_enums_and_boolean_sizes_return_safe_json_errors(self) -> None:
        self.init_receipt()
        baseline = json.loads(self.receipt.read_text(encoding="utf-8"))
        corruptions = {
            "provider_type": lambda data: data.__setitem__("provider", []),
            "boolean_size": lambda data: data["artifact"].__setitem__("size", True),
        }
        for name, corrupt in corruptions.items():
            with self.subTest(corruption=name):
                candidate = json.loads(json.dumps(baseline))
                corrupt(candidate)
                self.receipt.write_text(
                    json.dumps(candidate), encoding="utf-8"
                )
                result = self.run_cli(
                    "show", "--file", str(self.receipt), expected_code=2
                )
                self.assertFalse(result["ok"])

    def test_unexpected_field_names_are_not_echoed(self) -> None:
        self.init_receipt()
        data = json.loads(self.receipt.read_text(encoding="utf-8"))
        synthetic_key = "token=SYNTHETIC_PROTECTED_KEY"
        synthetic_value = "SYNTHETIC_PROTECTED_VALUE"
        data[synthetic_key] = synthetic_value
        self.receipt.write_text(json.dumps(data), encoding="utf-8")

        result = self.run_cli("show", "--file", str(self.receipt), expected_code=2)
        self.assertEqual(result["error"], "receipt has unexpected fields")
        self.assertNotIn(synthetic_key, json.dumps(result))
        self.assertNotIn(synthetic_value, json.dumps(result))

    def test_invalid_url_returns_safe_json_error_without_recording_event(self) -> None:
        self.init_receipt()
        malformed_url = "https://[SYNTHETIC_PRIVATE_HOST"
        result = self.run_cli(
            "record",
            "--file",
            str(self.receipt),
            "--event-id",
            "invalid-url",
            "--phase",
            "blocked",
            "--status",
            malformed_url,
            expected_code=2,
        )
        self.assertEqual(result["error"], "event.status contains an invalid URL")
        self.assertNotIn(malformed_url, json.dumps(result))
        shown = self.run_cli("show", "--file", str(self.receipt))
        self.assertEqual(shown["receipt"]["events"], [])

    def test_invalid_utf8_receipt_returns_safe_json_error(self) -> None:
        self.receipt.write_bytes(b'\xff{"SYNTHETIC_PRIVATE_KEY":"SYNTHETIC_PRIVATE_VALUE"}')
        result = self.run_cli("show", "--file", str(self.receipt), expected_code=2)
        self.assertEqual(result["error"], "receipt file is unreadable or invalid JSON")
        self.assertNotIn("SYNTHETIC_PRIVATE", json.dumps(result))
        self.assertNotIn(str(self.receipt), json.dumps(result))


if __name__ == "__main__":
    unittest.main()
