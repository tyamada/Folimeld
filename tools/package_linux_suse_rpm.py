"""Package a standalone build for openSUSE Leap 16.1 in an isolated copy."""
import argparse
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from tools.package_linux_rpm import build, refuse_existing  # noqa: E402


def package_name(version, revision, release, arch):
    if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", version):
        raise ValueError("Use a numeric major.minor.patch application version")
    if not re.fullmatch(r"[1-9][0-9]*", revision):
        raise ValueError("RPM revision must be a positive integer")
    if release != "16.1":
        raise ValueError("This recipe targets openSUSE Leap 16.1 only")
    if arch not in {"x86_64", "aarch64"}:
        raise ValueError(f"Unsupported RPM architecture: {arch}")
    return f"folimeld-{version}-{revision}.lp161.{arch}.rpm"


def context(root):
    if platform.system() != "Linux":
        raise ValueError("SUSE RPM packaging must run on Linux")
    release = platform.freedesktop_os_release()
    if release.get("ID") != "opensuse-leap" or release.get("VERSION_ID") != "16.1":
        raise ValueError("This recipe targets openSUSE Leap 16.1 only")
    for tool in ("rpmbuild", "rpm", "getconf"):
        if shutil.which(tool) is None:
            raise ValueError(f"SUSE RPM packaging requires {tool}")
    from folimeld import __version__
    arch = subprocess.check_output(["rpm", "--eval", "%{_arch}"], text=True).strip()
    revision = os.environ.get("FOLIMELD_RPM_REVISION", "1")
    name = package_name(__version__, revision, release["VERSION_ID"], arch)
    directory = Path(os.environ.get("FOLIMELD_LINUX_OUTPUT") or
                     root / "releases/opensuse-leap/16.1" / arch).resolve()
    package = directory / name
    refuse_existing(package)
    return package, {"VERSION": __version__, "REVISION": revision, "DIST_RELEASE": "lp161",
                     "LIBC_VERSION": subprocess.check_output(
                         ["getconf", "GNU_LIBC_VERSION"], text=True).split()[1]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    package, values = context(root)
    if args.check:
        print(package)
    else:
        print(f"Built SUSE package: {build(root, package, values, 'folimeld-suse.spec.in')}")


if __name__ == "__main__":
    main()
