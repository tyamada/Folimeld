from pathlib import Path
import unittest
from unittest.mock import patch

from tools.package_linux_tumbleweed_rpm import context, package_name


class TumbleweedRpmTests(unittest.TestCase):
    def test_snapshot_and_revision_outputs_do_not_collide(self):
        names = {package_name("0.3.3", revision, snapshot, "x86_64")
                 for revision in ("1", "2") for snapshot in ("20261102", "20261110")}
        self.assertEqual(len(names), 4)
        self.assertIn("folimeld-0.3.3-1.tw20261102.x86_64.rpm", names)

    def test_invalid_snapshot_and_injected_values_are_rejected(self):
        for args in [("0.3.3", "1", "16.1", "x86_64"),
                     ("0.3.3", "1", "20260230", "x86_64"),
                     ("0.3.3", "1", "20261110/../", "x86_64"),
                     ("0.3.3", "../1", "20261110", "x86_64"),
                     ("0.3.3\nRequires: other", "1", "20261110", "x86_64"),
                     ("0.3.3", "1", "20261110", "i686")]:
            with self.subTest(args=args), self.assertRaises(ValueError):
                package_name(*args)

    def test_other_rpm_distributions_are_rejected(self):
        for distro in ("fedora", "opensuse-leap", "sles"):
            with self.subTest(distro=distro), \
                 patch("tools.package_linux_tumbleweed_rpm.platform.system", return_value="Linux"), \
                 patch("tools.package_linux_tumbleweed_rpm.platform.freedesktop_os_release",
                       return_value={"ID": distro, "VERSION_ID": "20261110"}), \
                 self.assertRaisesRegex(ValueError, "Tumbleweed only"):
                context(Path.cwd())

    def test_non_linux_host_is_rejected(self):
        with patch("tools.package_linux_tumbleweed_rpm.platform.system", return_value="Windows"), \
             self.assertRaisesRegex(ValueError, "must run on Linux"):
            context(Path.cwd())
