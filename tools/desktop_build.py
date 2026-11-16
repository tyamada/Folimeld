"""Desktop build preflight. No compiler runs without explicitly calling main."""
import argparse
import hashlib
from importlib.metadata import version
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import struct
from urllib.parse import unquote, urlsplit

from tools.windows_build_environment import build_environment
from tools.desktop_crt import load_crt_manifest, verify_crt_inputs
from tools.desktop_inno import load_inno_manifest, verify_inno_inputs
from tools.desktop_runtime_terms import verify_runtime_terms


def reviewed_legal_datas(root: Path, arch: str = "x64") -> list[tuple[str, str]]:
    manifest = json.loads((root / "reviewed-files.json").read_text(encoding="utf-8"))
    required = {"Installed-packages.txt", "THIRD-PARTY-NOTICES.txt", "DEPENDENCY-SOURCES.json"}
    files = manifest.get("files", {})
    expected_dist = f"windows-desktop-{arch}"
    if manifest.get("distribution") != expected_dist or not required <= files.keys():
        raise ValueError("Desktop-specific reviewed license/source records are required.")
    result = []
    for name, expected in sorted(files.items()):
        relative = Path(name)
        path = (root / relative).resolve()
        if relative.is_absolute() or ".." in relative.parts or not path.is_relative_to(root.resolve()):
            raise ValueError("Unsafe legal input path.")
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected.lower():
            raise ValueError("Desktop legal input hash mismatch.")
        result.append((str(path), str(Path("licenses") / relative.parent)))
    return result


def _validate_wheel_input(name: str, pin: str, wheel: dict, kind: str) -> None:
    error = f"Invalid Desktop {kind} input: {name}"
    if not isinstance(wheel, dict):
        raise ValueError(error)
    digest = wheel.get("sha256")
    filename = wheel.get("filename")
    url = wheel.get("url")
    if (wheel.get("version") != pin or not isinstance(digest, str)
            or not re.fullmatch(r"[0-9a-f]{64}", digest)
            or not isinstance(filename, str)
            or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.+-]*\.whl", filename)
            or not isinstance(url, str) or any(c.isspace() or ord(c) < 32 or ord(c) == 127 for c in url)):
        raise ValueError(error)
    try:
        parts = urlsplit(url)
        path = unquote(parts.path)
        valid = (parts.scheme == "https" and parts.netloc == "files.pythonhosted.org"
                 and not parts.query and not parts.fragment and "?" not in url and "#" not in url
                 and path.startswith("/packages/") and "\\" not in path
                 and not any(c.isspace() or ord(c) < 32 or ord(c) == 127 for c in path)
                 and not {".", ".."}.intersection(path.split("/"))
                 and path.rsplit("/", 1)[-1] == filename)
    except ValueError:
        valid = False
    if not valid:
        raise ValueError(error)


def verify_desktop_requirements(root: Path, profile: dict, arch: str = "x64") -> dict[str, str]:
    """Accept only the two hash-locked direct-wheel lists; no pip execution."""
    verified = {}
    runtime_req = "desktop-arm64-runtime-requirements.txt" if arch == "arm64" else "desktop-runtime-requirements.txt"
    tools_req = "desktop-arm64-tools-requirements.txt" if arch == "arm64" else "desktop-tools-requirements.txt"
    for section, filename in (("wheels", runtime_req),
                              ("tool_wheels", tools_req)):
        path = root / "packaging/windows" / filename
        raw = path.read_bytes()
        entries = {}
        flags = set()
        for line in raw.decode("utf-8-sig").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line in {"--require-hashes", "--only-binary=:all:"}:
                if line in flags:
                    raise ValueError(f"Duplicate Desktop requirements option: {filename}")
                flags.add(line)
                continue
            match = re.fullmatch(
                r"([A-Za-z0-9][A-Za-z0-9_.-]*)[ \t]+@[ \t]+(\S+)[ \t]+--hash=sha256:([0-9a-f]{64})", line)
            if not match:
                raise ValueError(f"Invalid Desktop requirements line: {filename}")
            name, url, digest = match.groups()
            name = re.sub(r"[-_.]+", "-", name).lower()
            if name in entries:
                raise ValueError(f"Duplicate Desktop requirement: {name}")
            entries[name] = (url, digest)
        if flags != {"--require-hashes", "--only-binary=:all:"}:
            raise ValueError(f"Missing Desktop requirements options: {filename}")
        expected = {re.sub(r"[-_.]+", "-", name).lower(): (wheel["url"], wheel["sha256"])
                    for name, wheel in profile[section].items()}
        if len(expected) != len(profile[section]) or entries != expected:
            raise ValueError(f"Desktop requirements/JSON mismatch: {filename}")
        verified[filename] = hashlib.sha256(raw).hexdigest()
    return verified


def load_desktop_inputs(root: Path, arch: str = "x64") -> tuple[dict, dict, str]:
    manifest_name = "packaging/windows/desktop-arm64-runtime.json" if arch == "arm64" else "packaging/windows/desktop-runtime.json"
    path = root / manifest_name
    data = path.read_bytes()
    profile = json.loads(data)
    expected_dist = f"windows-desktop-{arch}"
    expected_plat = "windows-arm64" if arch == "arm64" else "windows-x86_64"
    if (profile.get("schema_version") != 1
            or profile.get("distribution") != expected_dist
            or profile.get("platform") != expected_plat
            or "uv" in profile):
        raise ValueError("Invalid Desktop fixed inputs.")
    if set(profile["wheels"]) != set(profile["dependencies"]):
        raise ValueError("Incomplete Desktop wheel ledger.")
    for name, pin in profile["dependencies"].items():
        _validate_wheel_input(name, pin, profile["wheels"][name], "wheel")
    if set(profile["tool_wheels"]) != set(profile["build_tools"]):
        raise ValueError("Incomplete Desktop tool wheel ledger.")
    for name, pin in profile["build_tools"].items():
        _validate_wheel_input(name, pin, profile["tool_wheels"][name], "tool")
    verify_desktop_requirements(root, profile, arch=arch)
    pins = dict(profile["dependencies"], **profile["build_tools"])
    return profile, pins, hashlib.sha256(data).hexdigest()


def verify_desktop_archives(profile: dict, input_root: Path) -> dict[str, str]:
    """Read-only hash gate; does not download, install or run any archive."""
    root = input_root.resolve(strict=True)
    entries = [dict(profile["python"], filename=profile["python"]["archive"]),
               *profile["wheels"].values(), *profile["tool_wheels"].values(),
               profile["inno_compiler"]]
    verified = {}
    for entry in entries:
        name = entry["filename"]
        path = (root / name).resolve(strict=True)
        if Path(name).name != name or not path.is_relative_to(root) or not path.is_file():
            raise ValueError("Unsafe Desktop archive path.")
        with path.open("rb") as source:
            digest = hashlib.file_digest(source, "sha256").hexdigest()
        if digest != entry["sha256"]:
            raise ValueError(f"Desktop archive hash mismatch: {name}")
        if "bytes" in entry and path.stat().st_size != entry["bytes"]:
            raise ValueError(f"Desktop archive size mismatch: {name}")
        verified[name] = digest
    return verified


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--legal-root", type=Path, required=True)
    parser.add_argument("--version-info", type=Path, required=True)
    parser.add_argument("--input-root", type=Path, required=True)
    parser.add_argument("--crt-root", type=Path, required=True)
    parser.add_argument("--inno-root", type=Path, required=True)
    parser.add_argument("--arch", choices=["x64", "arm64"], default="x64")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    expected_machine = {"arm64", "aarch64"} if args.arch == "arm64" else {"amd64", "x86_64"}
    if (sys.platform != "win32" or struct.calcsize("P") != 8
            or platform.machine().lower() not in expected_machine):
        raise RuntimeError(f"Build on Windows {args.arch}.")
    profile, pins, profile_hash = load_desktop_inputs(root, arch=args.arch)
    requirements_hashes = verify_desktop_requirements(root, profile, arch=args.arch)
    if platform.python_version() != profile["python"]["version"]:
        raise RuntimeError(f"Desktop build requires CPython {profile['python']['version']}.")
    for name, pin in pins.items():
        if version(name) != pin:
            raise RuntimeError(f"Build dependency drift: {name}")
    verified_archives = verify_desktop_archives(profile, args.input_root)
    crt_manifest, crt_manifest_hash = load_crt_manifest(root, arch=args.arch)
    crt_inputs = verify_crt_inputs(args.crt_root, crt_manifest, arch=args.arch)
    inno_manifest, inno_manifest_hash = load_inno_manifest(root, arch=args.arch)
    iss_file = root / "packaging/windows/Folimeld-desktop-arm64.iss" if args.arch == "arm64" else root / "packaging/windows/Folimeld-desktop.iss"
    inno_inputs = verify_inno_inputs(args.inno_root, inno_manifest, iss_file, arch=args.arch)
    reviewed_legal_datas(args.legal_root, arch=args.arch)
    runtime_terms = verify_runtime_terms(args.legal_root, arch=args.arch)
    if not args.version_info.is_file():
        raise FileNotFoundError(args.version_info)
    output = args.output.resolve()
    if output.exists():
        raise FileExistsError("Use a new Desktop build output directory.")
    output.mkdir(parents=True)
    environment = build_environment(os.environ, executable=sys.executable,
        base_prefix=sys.base_prefix, git_executable=shutil.which("git"))
    environment["FOLIMELD_DESKTOP_ARCH"] = args.arch
    environment["FOLIMELD_DESKTOP_CRT_ROOT"] = str(args.crt_root.resolve())
    environment["FOLIMELD_DESKTOP_LEGAL_ROOT"] = str(args.legal_root.resolve())
    environment["FOLIMELD_DESKTOP_VERSION_INFO"] = str(args.version_info.resolve())
    (output / "build-inputs.json").write_text(json.dumps({"python": sys.version,
        "pins": pins, "desktop_inputs_sha256": profile_hash,
        "verified_archives": verified_archives,
        "requirements_sha256": requirements_hashes,
        "inno_manifest_sha256": inno_manifest_hash, "inno_inputs": inno_inputs,
        "runtime_terms": runtime_terms, "crt_manifest_sha256": crt_manifest_hash, "crt_inputs": crt_inputs, "legal_root": str(args.legal_root.resolve()),
        "version_info_sha256": hashlib.sha256(args.version_info.read_bytes()).hexdigest()}, indent=2), encoding="utf-8")
    with (output / "pyinstaller.log").open("w", encoding="utf-8") as log:
        return subprocess.run([sys.executable, "-m", "PyInstaller", "--clean",
            "--distpath", str(output / "dist"), "--workpath", str(output / "work"),
            "Folimeld-desktop.spec"], cwd=root, env=environment, stdout=log,
            stderr=subprocess.STDOUT, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
