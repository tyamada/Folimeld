from pathlib import Path
import sys
import json
import tomllib

from folimeld import __version__
import unittest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "tools"))

from write_version_info import version_info, windows_version


class VersionInfoTests(unittest.TestCase):
    def test_windows_candidate_versions_are_consistent(self) -> None:
        candidate = json.loads((PROJECT_ROOT / "packaging/windows/release-candidate.json").read_text(encoding="utf-8"))
        project = tomllib.loads((PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
        self.assertEqual(candidate["status"], "candidate-not-built")
        self.assertEqual(candidate["app_version"], __version__)
        self.assertEqual(project["project"]["version"], __version__)
        self.assertEqual(candidate["architectures"], ["x64", "arm64"])
        self.assertEqual(windows_version(__version__), (0, 3, 11, 0))
        self.assertEqual(candidate["desktop"]["package_version"], "0.3.11.0")
        for channel in ("uv_source", "uv_tool"):
            self.assertEqual(candidate[channel]["version"], __version__)
        for channel in ("desktop", "uv_source", "uv_tool"):
            self.assertEqual(candidate[channel]["release_label"], "preview.1")
        store = candidate["store"]
        self.assertEqual(store["package_version"], "1.0.8.0")
        self.assertGreater(tuple(map(int, store["package_version"].split("."))),
                           tuple(map(int, store["previous_package_version"].split("."))))
        self.assertEqual(store["identity_name"], "TakumaYamada.Folimeld")
        self.assertEqual(store["publisher"], "CN=B897C2D7-6B65-499A-A779-BF572E2D81ED")

    def test_windows_version_adds_revision(self) -> None:
        self.assertEqual(windows_version("1.2.3"), (1, 2, 3, 0))

    def test_generated_resource_uses_same_version(self) -> None:
        generated = version_info("1.2.3")
        self.assertIn("filevers=(1, 2, 3, 0)", generated)
        self.assertIn("StringStruct(u'ProductVersion', u'1.2.3')", generated)

    def test_invalid_version_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            windows_version("1.2")


if __name__ == "__main__":
    unittest.main()
