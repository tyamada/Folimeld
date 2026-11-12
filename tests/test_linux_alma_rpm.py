from pathlib import Path
import unittest
from unittest.mock import patch

from tools.package_linux_alma_rpm import context, package_name


class AlmaRpmTests(unittest.TestCase):
    def test_output_distinguishes_minor_release_and_revision(self):
        names = {package_name("0.3.3", revision, release, "x86_64")
                 for revision in ("1", "2") for release in ("9.7", "9.8")}
        self.assertEqual(len(names), 4)
        self.assertIn("folimeld-0.3.3-1.alma9_8.x86_64.rpm", names)

    def test_invalid_values_are_rejected(self):
        for args in [("0.3.3", "1", "10.1", "x86_64"),
                     ("0.3.3", "1", "9/../", "x86_64"),
                     ("0.3.3", "../1", "9.8", "x86_64"),
                     ("0.3.3\nRequires: other", "1", "9.8", "x86_64"),
                     ("0.3.3", "1", "9.8", "i686")]:
            with self.subTest(args=args), self.assertRaises(ValueError):
                package_name(*args)

    def test_other_el_distributions_and_major_versions_are_rejected(self):
        for distro, version in [("rhel", "9.8"), ("rocky", "9.8"),
                                ("almalinux", "10.1"), ("fedora", "45")]:
            with self.subTest(distro=distro), \
                 patch("tools.package_linux_alma_rpm.platform.system", return_value="Linux"), \
                 patch("tools.package_linux_alma_rpm.platform.freedesktop_os_release",
                       return_value={"ID": distro, "VERSION_ID": version}), \
                 self.assertRaisesRegex(ValueError, "AlmaLinux 9 only"):
                context(Path.cwd())

    def test_non_linux_host_is_rejected(self):
        with patch("tools.package_linux_alma_rpm.platform.system", return_value="Windows"), \
             self.assertRaisesRegex(ValueError, "must run on Linux"):
            context(Path.cwd())
