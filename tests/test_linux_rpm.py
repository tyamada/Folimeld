from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tools.package_linux_rpm import context, package_name, refuse_existing


class FedoraRpmTests(unittest.TestCase):
    def test_output_distinguishes_release_arch_and_revision(self):
        names = {package_name("0.3.3", revision, release, arch)
                 for revision in ("1", "2") for release in ("44", "45")
                 for arch in ("x86_64", "aarch64")}
        self.assertEqual(len(names), 8)
        self.assertIn("folimeld-0.3.3-1.fc45.x86_64.rpm", names)

    def test_rejects_template_or_path_injection(self):
        invalid = [("0.3.3\nRequires: other", "1", "45", "x86_64"),
                   ("0.3.3", "../2", "45", "x86_64"),
                   ("0.3.3", "0", "45", "x86_64"),
                   ("0.3.3", "1", "rawhide", "x86_64"),
                   ("0.3.3", "1", "45", "i686")]
        for args in invalid:
            with self.subTest(args=args), self.assertRaises(ValueError):
                package_name(*args)

    def test_existing_package_is_unchanged(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "existing.rpm"
            path.write_bytes(b"previous package")
            with self.assertRaises(FileExistsError):
                refuse_existing(path)
            self.assertEqual(path.read_bytes(), b"previous package")

    def test_dangling_output_symlink_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "existing.rpm"
            try:
                path.symlink_to("missing-target")
            except OSError:
                self.skipTest("Symlinks unavailable")
            with self.assertRaises(FileExistsError):
                refuse_existing(path)
            self.assertTrue(path.is_symlink())

    def test_fedora_recipe_is_not_used_on_other_rpm_distributions(self):
        for distro in ("ubuntu", "opensuse-leap", "almalinux"):
            with self.subTest(distro=distro), \
                 patch("tools.package_linux_rpm.platform.system", return_value="Linux"), \
                 patch("tools.package_linux_rpm.platform.freedesktop_os_release",
                       return_value={"ID": distro, "VERSION_ID": "45"}), \
                 self.assertRaisesRegex(ValueError, "Fedora-only"):
                context(Path.cwd())

    def test_rejects_non_linux_host(self):
        with patch("tools.package_linux_rpm.platform.system", return_value="Windows"), \
             self.assertRaisesRegex(ValueError, "Fedora Linux"):
            context(Path.cwd())


if __name__ == "__main__":
    unittest.main()
