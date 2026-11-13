from pathlib import Path
from importlib.metadata import PackageNotFoundError
from types import SimpleNamespace
import tempfile
import unittest
from unittest.mock import patch

from folimeld.license_info import installed_notices, license_documents
from tools.license_bundle import license_datas


class LicenseInfoTests(unittest.TestCase):
    def test_source_run_without_winrt_metadata_still_loads_documents(self):
        def lookup(name):
            if name.startswith("winrt"):
                raise PackageNotFoundError(name)
            return SimpleNamespace(version="1.2", metadata={"License": "Test license"}, files=[])

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "licenses").mkdir()
            (root / "LICENSE").write_text("Folimeld notice", encoding="utf-8")
            (root / "licenses" / "AGPL-3.0.txt").write_text("AGPL notice", encoding="utf-8")
            with patch("sys._MEIPASS", directory, create=True), \
                    patch("sys.frozen", False, create=True), \
                    patch("folimeld.license_info.sys.platform", "win32"), \
                    patch("folimeld.license_info.distribution", side_effect=lookup):
                documents = dict(license_documents())
        self.assertIn("AGPL-3.0", documents)
        self.assertIn("PySide6 1.2", documents["Installed-packages"])
        self.assertIn("cryptography 1.2", documents["Installed-packages"])
        self.assertIn("cffi 1.2", documents["Installed-packages"])
        self.assertIn("pycparser 1.2", documents["Installed-packages"])
        self.assertIn("winrt-runtime: package metadata is not available", documents["Installed-packages"])

    def test_packaging_still_rejects_missing_metadata(self):
        with patch("folimeld.license_info.distribution", side_effect=PackageNotFoundError("missing")):
            with self.assertRaises(PackageNotFoundError):
                installed_notices()

    def test_monolithic_pyside_allows_absent_splits_but_declared_splits_remain_required(self):
        for split_required in (False, True):
            with self.subTest(split_required=split_required):
                def lookup(name):
                    if name in {"PySide6_Essentials", "PySide6_Addons"}:
                        raise PackageNotFoundError(name)
                    return SimpleNamespace(
                        version="6.11.2", metadata={}, files=[],
                        requires=["PySide6-Essentials==6.11.2"] if split_required else [],
                    )

                with patch("folimeld.license_info.distribution", side_effect=lookup), \
                        patch("folimeld.license_info.Path.exists", return_value=True), \
                        patch("folimeld.license_info.Path.read_text", return_value="Python notice"):
                    if split_required:
                        with self.assertRaises(PackageNotFoundError):
                            installed_notices()
                    else:
                        self.assertIn("not used by this monolithic PySide6", installed_notices())

    def test_packaging_includes_bootloader_license_text(self):
        with tempfile.TemporaryDirectory() as directory:
            copying = Path(directory) / "COPYING.txt"
            text = "Bootloader license\nSpecial exception for distributed executables.\n"
            copying.write_text(text, encoding="utf-8")

            def lookup(name):
                return SimpleNamespace(
                    version="6.22.2", metadata={},
                    files=[Path("licenses/COPYING.txt")] if name == "PyInstaller" else [],
                    locate_file=lambda file: copying,
                )

            with patch("folimeld.license_info.distribution", side_effect=lookup):
                notices = installed_notices()
            self.assertIn("PyInstaller 6.22.2", notices)
            self.assertIn(text, notices)

    def test_source_run_tolerates_missing_python_license_but_packaging_does_not(self):
        package = SimpleNamespace(version="1.2", metadata={}, files=[])
        with patch("folimeld.license_info.distribution", return_value=package), \
                patch("folimeld.license_info.Path.exists", return_value=False):
            self.assertIn("LICENSE.txt is not available", installed_notices(strict=False))
            with self.assertRaises(FileNotFoundError):
                installed_notices()

    def test_frozen_app_reads_bundled_documents_without_package_metadata(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "licenses").mkdir()
            (root / "LICENSE").write_text("Folimeld notice", encoding="utf-8")
            (root / "licenses" / "AGPL-3.0.txt").write_text("Full license", encoding="utf-8")
            (root / "licenses" / "Installed-packages.txt").write_text("Bundled versions", encoding="utf-8")
            with patch("sys._MEIPASS", directory, create=True), patch("sys.frozen", True, create=True), \
                    patch("folimeld.license_info.installed_notices", side_effect=AssertionError):
                documents = dict(license_documents())
            self.assertEqual(documents["Installed-packages"], "Bundled versions")
            self.assertEqual(documents["AGPL-3.0"], "Full license")

    def test_bundle_collects_build_environment_notices(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch("tools.license_bundle.installed_notices", return_value="Package 1.2\nNotice"):
                data = license_datas(directory)
            source, destination = data[-1]
            self.assertEqual(destination, "licenses")
            self.assertEqual(Path(source).read_text(encoding="utf-8"), "Package 1.2\nNotice")


if __name__ == "__main__":
    unittest.main()
