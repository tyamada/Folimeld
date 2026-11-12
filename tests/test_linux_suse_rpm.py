from pathlib import Path
import unittest
from unittest.mock import patch

from tools.package_linux_suse_rpm import context, package_name


class SuseRpmTests(unittest.TestCase):
    def test_output_identifies_leap_and_revision(self):
        self.assertEqual(package_name("0.3.3", "2", "16.1", "x86_64"),
                         "folimeld-0.3.3-2.lp161.x86_64.rpm")

    def test_rejects_other_releases_and_injected_values(self):
        for args in [("0.3.3", "1", "16.0", "x86_64"),
                     ("0.3.3", "1", "20261112", "x86_64"),
                     ("0.3.3", "../2", "16.1", "x86_64"),
                     ("0.3.3\nRequires: other", "1", "16.1", "x86_64"),
                     ("0.3.3", "1", "16.1", "i686")]:
            with self.subTest(args=args), self.assertRaises(ValueError):
                package_name(*args)

    def test_rejects_other_rpm_distributions(self):
        for distro, version in [("fedora", "44"), ("opensuse-tumbleweed", "20261112"),
                                ("opensuse-leap", "16.0"), ("sles", "16.1")]:
            with self.subTest(distro=distro), \
                 patch("tools.package_linux_suse_rpm.platform.system", return_value="Linux"), \
                 patch("tools.package_linux_suse_rpm.platform.freedesktop_os_release",
                       return_value={"ID": distro, "VERSION_ID": version}), \
                 self.assertRaisesRegex(ValueError, "Leap 16.1 only"):
                context(Path.cwd())

    def test_rejects_non_linux_host(self):
        with patch("tools.package_linux_suse_rpm.platform.system", return_value="Windows"), \
             self.assertRaisesRegex(ValueError, "must run on Linux"):
            context(Path.cwd())
