#!/usr/bin/env python3
"""Demonstrate receipt recovery with synthetic data; no accounts or network."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).with_name("delivery_receipt.py")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="delivery-demo-") as directory:
        root = Path(directory)
        artifact, metadata, receipt = (root / name for name in ("video.bin", "intent.json", "receipt.json"))
        artifact.write_bytes(b"synthetic video fixture\n")
        metadata.write_text('{"audience":"private","notify":false}\n', encoding="utf-8")

        def call(*args: str, expected: int = 0) -> dict:
            result = subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True, check=False)
            value = json.loads(result.stdout)
            if result.returncode != expected:
                raise RuntimeError("unexpected receipt result: " + str(value.get("error", result.returncode)))
            return value

        call("init", "--file", str(receipt), "--delivery-id", "example-1", "--provider", "youtube",
             "--provider-account-id", "example-channel", "--release-id", "example-video-1", "--target-kind", "video",
             "--target-id", "example-video-1", "--channel", "private", "--effect", "stage", "--release-mode", "private",
             "--artifact", str(artifact), "--metadata-file", str(metadata))
        event = ("record", "--file", str(receipt), "--event-id", "upload-1", "--phase", "processing", "--status", "processing",
                 "--observed-at", "2026-01-01T12:00:00Z", "--provider-object-kind", "video", "--provider-object-id", "example-video-1",
                 "--next-action", "Read provider state before retrying")
        call(*event)
        repeated = call(*event)
        validated = call("validate", "--file", str(receipt), "--artifact", str(artifact), "--metadata-file", str(metadata))
        artifact.write_bytes(b"changed bytes\n")
        changed = call("validate", "--file", str(receipt), "--artifact", str(artifact), "--metadata-file", str(metadata), expected=2)
        print("Delivery / synthetic recovery demo")
        print("  1. Bound artifact and intent to one private staging request.")
        print("  2. Recorded processing; no release or verification was inferred.")
        print("  3. Replayed observation: " + repeated["status"] + ".")
        print("  4. Revalidated original files: " + str(validated["complete"]).lower() + ".")
        print("  5. Changed artifact rejected: " + changed["error"] + ".")
        print("No provider was contacted. Temporary files are removed on exit.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
