"""Synthetic regression tests for the package's privacy and resource boundary."""
from __future__ import annotations

import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location("delivery_package", Path(__file__).resolve().parents[1] / "scripts/validate_package.py")
assert SPEC is not None and SPEC.loader is not None
PACKAGE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PACKAGE)


class PackageTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="delivery-package-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "package"
        self.root.mkdir()
        self.manifest = {
            "name": "delivery", "version": "0.3.0", "license": "MIT",
            "repository": "https://github.com/example/delivery",
            "homepage": "https://github.com/example/delivery", "skills": "./skills/",
            "interface": {"websiteURL": "https://github.com/example/delivery", "logo": "./assets/icon.png", "composerIcon": "./assets/icon.png"},
        }
        self.marketplace = {"name": "delivery", "plugins": [{
            "name": "delivery", "source": "./", "version": "0.3.0",
            "repository": "https://github.com/example/delivery", "license": "MIT",
        }]}
        for host in (".codex-plugin", ".claude-plugin"):
            self.write_json(host + "/plugin.json", self.manifest)
        self.write_json(".claude-plugin/marketplace.json", self.marketplace)
        self.write("assets/icon.png", PACKAGE.PNG_HEADER)
        for required in ("README.md", "LICENSE", "CONTRIBUTING.md", "SECURITY.md", "CHANGELOG.md", "scripts/delivery_receipt.py"):
            self.write(required, "Synthetic fixture.\n")
        self.write("skills/delivery/SKILL.md", "---\nname: delivery\ndescription: Synthetic delivery fixture.\n---\n[Guide](../../README.md)\n")

    def write(self, relative: str, value: str | bytes) -> None:
        target = self.root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(value, bytes):
            target.write_bytes(value)
        else:
            target.write_text(value, encoding="utf-8")

    def write_json(self, relative: str, value: object) -> None:
        self.write(relative, json.dumps(value))

    def test_complete_package_and_optional_native_marketplace(self) -> None:
        errors, counts = PACKAGE.validate(self.root)
        self.assertEqual(errors, [])
        self.assertEqual(counts["skills"], 1)
        self.assertEqual(counts["local_links"], 1)
        self.write_json(".agents/plugins/marketplace.json", {"name": "delivery", "plugins": [{
            "name": "delivery", "source": {"source": "local", "path": "."},
            "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
        }]})
        self.assertEqual(PACKAGE.validate(self.root)[0], [])

    def test_malformed_manifest_and_marketplace_types_fail_without_traceback(self) -> None:
        for value in (None, [], "invalid", 3, True):
            with self.subTest(interface=value):
                manifest = copy.deepcopy(self.manifest)
                manifest["interface"] = value
                self.write_json(".codex-plugin/plugin.json", manifest)
                self.assertTrue(PACKAGE.validate(self.root)[0])
            self.write_json(".codex-plugin/plugin.json", self.manifest)
            for relative in (".claude-plugin/marketplace.json", ".agents/plugins/marketplace.json"):
                with self.subTest(marketplace=relative, plugins=value):
                    self.write_json(relative, {"name": "delivery", "plugins": value})
                    self.assertTrue(PACKAGE.validate(self.root)[0])
                (self.root / relative).unlink()
                self.write_json(".claude-plugin/marketplace.json", self.marketplace)

    def test_duplicate_keys_and_binary_json_are_rejected(self) -> None:
        for value in ('{"name":"delivery","name":"other"}', '{"name":"delivery","extra":NaN}', b"\xff\xfe"):
            with self.subTest(value_type=type(value).__name__):
                self.write(".codex-plugin/plugin.json", value)
                errors, _ = PACKAGE.validate(self.root)
                self.assertTrue(errors)
                self.assertTrue(any("invalid JSON" in error for error in errors))

    def test_links_and_icons_cannot_escape_or_reference_missing_files(self) -> None:
        outside = self.root.parent / "outside.txt"
        outside.write_text("must not be loaded", encoding="utf-8")
        for target in ("../outside.txt", "%2e%2e/outside.txt", "missing.md", "../outside.txt#anchor", "../outside.txt?query=1"):
            with self.subTest(target=target):
                self.write("README.md", "[Resource](" + target + ")\n")
                errors, _ = PACKAGE.validate(self.root)
                self.assertTrue(any("local link" in error for error in errors))
                self.assertNotIn(target, "\n".join(errors))
        self.write("README.md", "[Ref][guide]\n[guide]: <missing document.md>\n")
        self.assertTrue(PACKAGE.validate(self.root)[0])
        self.write("tmp/generated.md", "Local build output.\n")
        self.write("README.md", "[Generated](tmp/generated.md)\n")
        self.assertTrue(PACKAGE.validate(self.root)[0])
        self.write("README.md", "`$PLUGIN_ROOT/../outside.txt`\n")
        self.assertTrue(PACKAGE.validate(self.root)[0])
        self.write("README.md", "Synthetic fixture.\n")
        manifest = copy.deepcopy(self.manifest)
        manifest["interface"]["logo"] = "../outside.txt"
        self.write_json(".codex-plugin/plugin.json", manifest)
        self.assertTrue(any("out-of-package logo" in error for error in PACKAGE.validate(self.root)[0]))

    def test_private_content_is_rejected_without_echoing_values(self) -> None:
        examples = (
            "gh" + "p_" + "a" * 30,
            "-----BEGIN " + "OPENSSH PRIVATE KEY-----",
            "Z:" + "/workstation/" + "private-project",
            "/home/" + "synthetic-person/private-project/",
        )
        for value in examples:
            with self.subTest(kind=examples.index(value)):
                self.write("README.md", "[Local](" + value + ")\n")
                errors, _ = PACKAGE.validate(self.root)
                self.assertTrue(errors)
                self.assertNotIn(value, "\n".join(errors))
                self.assertTrue(any("detected (value withheld)" in error for error in errors))

    def test_native_marketplace_cannot_redirect_or_force_install(self) -> None:
        for source, installation in (({"source": "local", "path": "../outside"}, "AVAILABLE"), ({"source": "local", "path": "."}, "INSTALLED_BY_DEFAULT")):
            with self.subTest(source=source, installation=installation):
                self.write_json(".agents/plugins/marketplace.json", {"name": "delivery", "plugins": [{
                    "name": "delivery", "source": source, "policy": {"installation": installation},
                }]})
                self.assertTrue(PACKAGE.validate(self.root)[0])

    def test_symlinked_resources_are_rejected(self) -> None:
        external = self.root.parent / "external.png"
        external.write_bytes(PACKAGE.PNG_HEADER)
        icon = self.root / "assets/icon.png"
        icon.unlink()
        try:
            icon.symlink_to(external)
        except OSError:
            self.skipTest("symlinks unavailable on this host")
        errors, _ = PACKAGE.validate(self.root)
        self.assertTrue(errors)
        self.assertNotIn(str(external), "\n".join(errors))


if __name__ == "__main__":
    unittest.main()
