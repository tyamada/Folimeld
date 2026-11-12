"""Package a standalone build on Fedora; never overwrite existing output."""
import argparse
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import tempfile


def package_name(version, revision, fedora, arch):
    if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", version):
        raise ValueError("Use a numeric major.minor.patch application version")
    if not re.fullmatch(r"[1-9][0-9]*", revision):
        raise ValueError("RPM revision must be a positive integer")
    if not re.fullmatch(r"[1-9][0-9]*", fedora):
        raise ValueError("Fedora version must be numeric (not Rawhide)")
    if arch not in {"x86_64", "aarch64"}:
        raise ValueError(f"Unsupported RPM architecture: {arch}")
    return f"folimeld-{version}-{revision}.fc{fedora}.{arch}.rpm"


def refuse_existing(path):
    if path.exists() or path.is_symlink():
        raise FileExistsError(f"Refusing to overwrite existing package: {path}")


def context(root, output=None):
    if platform.system() != "Linux":
        raise ValueError("RPM packaging must run on Fedora Linux")
    release = platform.freedesktop_os_release()
    if release.get("ID") != "fedora":
        raise ValueError("This RPM recipe is Fedora-only; build other RPM distributions separately")
    for tool in ("rpmbuild", "rpm", "getconf"):
        if shutil.which(tool) is None:
            raise ValueError(f"Fedora RPM packaging requires {tool}")
    # Importing __init__ does not import Qt or other runtime dependencies.
    import sys
    sys.path.insert(0, str(root))
    from folimeld import __version__
    fedora = release["VERSION_ID"]
    arch = subprocess.check_output(["rpm", "--eval", "%{_arch}"], text=True).strip()
    revision = os.environ.get("FOLIMELD_RPM_REVISION", "1")
    name = package_name(__version__, revision, fedora, arch)
    directory = Path(output or os.environ.get("FOLIMELD_LINUX_OUTPUT") or
                     root / "releases" / "fedora" / fedora / arch).resolve()
    package = directory / name
    refuse_existing(package)
    return package, {"VERSION": __version__, "REVISION": revision, "FEDORA": fedora,
                     "LIBC_VERSION": subprocess.check_output(
                         ["getconf", "GNU_LIBC_VERSION"], text=True).split()[1]}


def build(root, package, values, template="folimeld-fedora.spec.in"):
    inputs = {"folimeld": root / "dist/folimeld",
              "folimeld.desktop": root / "packaging/linux/folimeld.desktop",
              "folimeld.png": root / "assets/Folimeld.iconset/icon_256x256.png",
              "LICENSE": root / "LICENSE"}
    for source in inputs.values():
        if source.is_symlink() or not source.is_file():
            raise ValueError(f"Missing or symlinked packaging input: {source}")
    text = (root / "packaging/linux" / template).read_text(encoding="utf-8")
    for name, value in values.items():
        text = text.replace(f"@{name}@", value)
    if re.search(r"@[A-Z_]+@", text):
        raise ValueError("Unresolved RPM template value")
    # TMPDIR can place all temporary build/cleanup work inside an isolated copy.
    with tempfile.TemporaryDirectory(prefix="folimeld-rpm-") as temporary:
        top = Path(temporary)
        for name in ("SOURCES", "SPECS", "BUILD", "BUILDROOT", "RPMS", "SRPMS"):
            (top / name).mkdir()
        for name, source in inputs.items():
            shutil.copy2(source, top / "SOURCES" / name)
        spec = top / "SPECS/folimeld.spec"
        spec.write_text(text, encoding="utf-8")
        subprocess.run(["rpmbuild", "-bb", "--define", f"_topdir {top}", str(spec)], check=True)
        candidates = list((top / "RPMS").glob(f"*/{package.name}"))
        if len(candidates) != 1:
            raise ValueError("Expected exactly one RPM output")
        package.parent.mkdir(parents=True, exist_ok=True)
        # Exclusive creation also guards a competing build after preflight.
        with package.open("xb") as destination, candidates[0].open("rb") as source:
            shutil.copyfileobj(source, destination)
    from tools.source_bundle import record_artifact
    record_artifact(inputs["folimeld"], package, root / "dist/source", project_root=root)
    return package


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Validate platform/tools/output before building")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    package, values = context(root)
    if args.check:
        print(package)
    else:
        print(f"Built Fedora package: {build(root, package, values)}")


if __name__ == "__main__":
    main()
