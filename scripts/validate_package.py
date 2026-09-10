#!/usr/bin/env python3
"""Validate the portable package using only the Python standard library."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path, PureWindowsPath
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {".git", "__pycache__", ".pytest_cache", ".venv", "tmp", "dist", "build"}
LOCAL_PATH = re.compile(r"(?i)(?:\b[a-z]:[/\\]|/(?:Users|home)/[^\s/]+/|\\\\[a-z0-9_.-]+\\)")
TOKEN = re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{30,}|sk-[A-Za-z0-9_-]{24,}|(?:AKIA|ASIA)[A-Z0-9]{16})\b")
PRIVATE_KEY = re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")
PATTERNS = (("absolute local path", LOCAL_PATH), ("token-shaped data", TOKEN), ("private key", PRIVATE_KEY))
PNG_HEADER = b"\x89PNG\r\n\x1a\n"


def _json_object(pairs: list[tuple[str, object]]) -> dict:
    result: dict = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def _invalid_constant(_value: str) -> None:
    raise ValueError("non-finite JSON number")


def validate(root: Path) -> tuple[list[str], dict[str, int]]:
    root = root.resolve()
    errors: list[str] = []
    counts = {"skills": 0, "files": 0, "local_links": 0}

    def issue(path: Path, message: str) -> None:
        relative = path.relative_to(root).as_posix()
        if any(pattern.search(relative) for _, pattern in PATTERNS):
            relative = "(sensitive filename withheld)"
        errors.append(f"{relative}: {message}")

    def resource(owner: Path, base: Path, target: object, label: str) -> Path | None:
        if not isinstance(target, str) or not target.strip() or "\x00" in target:
            issue(owner, f"invalid {label} (value withheld)")
            return None
        try:
            decoded = unquote(target).replace("\\", "/")
            if Path(decoded).is_absolute() or PureWindowsPath(decoded).drive:
                raise ValueError("absolute resource")
            candidate = base / decoded
            resolved = candidate.resolve()
            if not resolved.is_relative_to(root) or not resolved.exists():
                raise ValueError("missing or escaping resource")
            if any(part in EXCLUDED for part in resolved.relative_to(root).parts):
                raise ValueError("resource is excluded from the package")
            if any(part.is_symlink() for part in (candidate, *candidate.parents) if part != root):
                raise ValueError("symlink resource")
            return resolved
        except (OSError, ValueError, RuntimeError):
            issue(owner, f"missing, unsafe, or out-of-package {label} (value withheld)")
            return None

    def read_json(path: Path) -> dict:
        safe = resource(path, root, path.relative_to(root).as_posix(), "JSON file")
        if safe is None:
            return {}
        try:
            value = json.loads(safe.read_text(encoding="utf-8"), object_pairs_hook=_json_object, parse_constant=_invalid_constant)
            if not isinstance(value, dict):
                raise ValueError("expected object")
            return value
        except (OSError, UnicodeError, ValueError, RecursionError):
            issue(path, "invalid JSON object (details withheld)")
            return {}

    manifests = [read_json(root / host / "plugin.json") for host in (".codex-plugin", ".claude-plugin")]
    codex = manifests[0]
    for index, manifest in enumerate(manifests):
        path = root / (".codex-plugin" if index == 0 else ".claude-plugin") / "plugin.json"
        if manifest.get("name") != "delivery":
            issue(path, "plugin name must be delivery")
        version = manifest.get("version")
        if not isinstance(version, str) or not re.fullmatch(r"\d+\.\d+\.\d+", version):
            issue(path, "version must be semantic major.minor.patch")
        for field in ("name", "version", "repository", "license"):
            if not isinstance(manifest.get(field), str) or not manifest[field] or manifest[field] != codex.get(field):
                issue(path, f"missing or inconsistent {field}")
        repository = manifest.get("repository")
        if not isinstance(repository, str) or not re.fullmatch(r"https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository):
            issue(path, "repository must identify one standalone GitHub repository")
        if manifest.get("homepage") != repository:
            issue(path, "homepage must identify this repository")
    interface = codex.get("interface")
    if not isinstance(interface, dict):
        issue(root / ".codex-plugin/plugin.json", "interface must be an object")
        interface = {}
    if interface.get("websiteURL") != codex.get("repository"):
        issue(root / ".codex-plugin/plugin.json", "website must identify this repository")
    if codex.get("skills") != "./skills/":
        issue(root / ".codex-plugin/plugin.json", "skills must bind the packaged skills directory")
    for field in ("composerIcon", "logo"):
        owner = root / ".codex-plugin/plugin.json"
        icon = resource(owner, root, interface.get(field), field)
        if icon is not None:
            try:
                with icon.open("rb") as stream:
                    if stream.read(8) != PNG_HEADER:
                        issue(owner, f"invalid PNG {field}")
            except OSError:
                issue(owner, f"unreadable PNG {field}")

    marketplace_path = root / ".claude-plugin/marketplace.json"
    marketplace = read_json(marketplace_path)
    entries = marketplace.get("plugins")
    if marketplace.get("name") != "delivery" or not isinstance(entries, list) or len(entries) != 1 or not isinstance(entries[0], dict):
        issue(marketplace_path, "expected one delivery marketplace entry")
    else:
        entry = entries[0]
        if entry.get("name") != "delivery" or entry.get("source") != "./" or entry.get("version") != codex.get("version"):
            issue(marketplace_path, "entry must bind the root plugin and current version")
        for field in ("repository", "license"):
            if entry.get(field) != codex.get(field):
                issue(marketplace_path, f"inconsistent {field}")

    native_path = root / ".agents/plugins/marketplace.json"
    if native_path.exists() or native_path.is_symlink():
        native = read_json(native_path)
        entries = native.get("plugins")
        if native.get("name") != "delivery" or not isinstance(entries, list) or len(entries) != 1 or not isinstance(entries[0], dict):
            issue(native_path, "expected one native delivery marketplace entry")
        else:
            entry = entries[0]
            if entry.get("name") != "delivery" or entry.get("source") != {"source": "local", "path": "."}:
                issue(native_path, "native entry must bind the repository root")
            policy = entry.get("policy")
            if not isinstance(policy, dict) or policy.get("installation") != "AVAILABLE":
                issue(native_path, "native installation must remain opt-in")

    for required in ("README.md", "LICENSE", "CONTRIBUTING.md", "SECURITY.md", "CHANGELOG.md", "scripts/delivery_receipt.py"):
        path = resource(root / required, root, required, "required package file")
        if path is not None and not path.is_file():
            issue(root / required, "required package file is not a regular file")

    skills = sorted((root / "skills").glob("*/SKILL.md"))
    counts["skills"] = len(skills)
    if not skills:
        issue(root / "skills", "no skills discovered")
    for skill in skills:
        safe = resource(skill, root, skill.relative_to(root).as_posix(), "skill file")
        if safe is None:
            continue
        try:
            text = safe.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            issue(skill, "skill must be readable UTF-8")
            continue
        parts = text.split("---", 2)
        if len(parts) != 3 or parts[0].strip():
            issue(skill, "missing YAML frontmatter")
            continue
        name = re.search(r"(?m)^name:\s*([a-z0-9-]+)\s*$", parts[1])
        if not name or name.group(1) != skill.parent.name:
            issue(skill, "frontmatter name must match skill folder")
        if not re.search(r"(?m)^description:\s*\S", parts[1]):
            issue(skill, "missing description")

    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)
        if any(part in EXCLUDED for part in rel.parts):
            continue
        if path.is_symlink():
            issue(path, "symlinks are not portable package files")
            continue
        if not path.is_file():
            continue
        counts["files"] += 1
        if path.name.startswith(".env") or path.suffix.lower() in {".p8", ".p12", ".pfx", ".jks", ".keystore", ".pem", ".key", ".pyc"}:
            issue(path, "private or generated file must not ship")
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeError:
            if path.suffix.lower() in {".md", ".json", ".py", ".yaml", ".yml", ".toml"}:
                issue(path, "text file must be UTF-8")
            continue
        except OSError:
            issue(path, "package file is unreadable")
            continue
        for label, pattern in PATTERNS:
            if pattern.search(text):
                issue(path, label + " detected (value withheld)")
        if path.suffix != ".md":
            continue
        targets = re.findall(r"!?\[[^\]]*\]\(\s*(<[^>]*>|[^\s)]+)(?:\s+[\"'][^\"']*[\"'])?\s*\)", text)
        targets += re.findall(r"(?m)^\s{0,3}\[[^\]]+\]:\s*(<[^>]*>|\S+)", text)
        targets += re.findall(r"(?:src|href)=[\"']([^\"']+)[\"']", text)
        for target in targets:
            target = target.strip("<>")
            if target.startswith("#"):
                continue
            try:
                parsed = urlsplit(target)
            except ValueError:
                issue(path, "invalid link (value withheld)")
                continue
            if parsed.scheme.lower() in {"http", "https", "mailto"}:
                continue
            if parsed.scheme or parsed.netloc:
                issue(path, "unsupported or nonportable link (value withheld)")
                continue
            resource(path, path.parent, parsed.path, "local link")
            counts["local_links"] += 1
        for target in re.findall(r"\$PLUGIN_ROOT/([A-Za-z0-9_./%-]+)", text):
            resource(path, root, target.rstrip("."), "bundled resource")
    return sorted(set(errors)), counts


def main() -> int:
    errors, counts = validate(ROOT)
    print(json.dumps({"ok": not errors, **counts, "errors": errors}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
