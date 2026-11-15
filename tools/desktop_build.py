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


def reviewed_legal_datas(root: Path) -> list[tuple[str, str]]:
    manifest = json.loads((root / "reviewed-files.json").read_text(encoding="utf-8"))
    required = {"Installed-packages.txt", "THIRD-PARTY-NOTICES.txt", "DEPENDENCY-SOURCES.json"}
    files = manifest.get("files", {})
    if manifest.get("distribution") != "windows-desktop-x64" or not required <= files.keys():
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


def verify_desktop_requirements(root: Path, profile: dict) -> dict[str, str]:
    """Accept only the two hash-locked direct-wheel lists; no pip execution."""
    verified = {}
    for section, filename in (("wheels", "desktop-runtime-requirements.txt"),
                              ("tool_wheels", "desktop-tools-requirements.txt")):
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


def load_desktop_inputs(root: Path) -> tuple[dict, dict, str]:
    path = root / "packaging/windows/desktop-runtime.json"
    data = path.read_bytes()
    profile = json.loads(data)
    if (profile.get("schema_version") != 1
            or profile.get("distribution") != "windows-desktop-x64"
            or profile.get("platform") != "windows-x86_64"
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
    verify_desktop_requirements(root, profile)
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
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    if (sys.platform != "win32" or struct.calcsize("P") != 8
            or platform.machine().lower() not in {"amd64", "x86_64"}):
        raise RuntimeError("Build on Windows x64.")
    profile, pins, profile_hash = load_desktop_inputs(root)
    requirements_hashes = verify_desktop_requirements(root, profile)
    if platform.python_version() != profile["python"]["version"]:
        raise RuntimeError("Desktop build requires CPython 3.12.16.")
    for name, pin in pins.items():
        if version(name) != pin:
            raise RuntimeError(f"Build dependency drift: {name}")
    verified_archives = verify_desktop_archives(profile, args.input_root)
    crt_manifest, crt_manifest_hash = load_crt_manifest(root)
    crt_inputs = verify_crt_inputs(args.crt_root, crt_manifest)
    inno_manifest, inno_manifest_hash = load_inno_manifest(root)
    inno_inputs = verify_inno_inputs(args.inno_root, inno_manifest, root / "packaging/windows/Folimeld-desktop.iss")
    reviewed_legal_datas(args.legal_root)
    if not args.version_info.is_file():
        raise FileNotFoundError(args.version_info)
    output = args.output.resolve()
    if output.exists():
        raise FileExistsError("Use a new Desktop build output directory.")
    output.mkdir(parents=True)
    environment = build_environment(os.environ, executable=sys.executable,
        base_prefix=sys.base_prefix, git_executable=shutil.which("git"))
    environment["FOLIMELD_DESKTOP_CRT_ROOT"] = str(args.crt_root.resolve())
    environment["FOLIMELD_DESKTOP_LEGAL_ROOT"] = str(args.legal_root.resolve())
    environment["FOLIMELD_DESKTOP_VERSION_INFO"] = str(args.version_info.resolve())
    (output / "build-inputs.json").write_text(json.dumps({"python": sys.version,
        "pins": pins, "desktop_inputs_sha256": profile_hash,
        "verified_archives": verified_archives,
        "requirements_sha256": requirements_hashes,
        "inno_manifest_sha256": inno_manifest_hash, "inno_inputs": inno_inputs,
        "crt_manifest_sha256": crt_manifest_hash, "crt_inputs": crt_inputs, "legal_root": str(args.legal_root.resolve()),
        "version_info_sha256": hashlib.sha256(args.version_info.read_bytes()).hexdigest()}, indent=2), encoding="utf-8")
    with (output / "pyinstaller.log").open("w", encoding="utf-8") as log:
        return subprocess.run([sys.executable, "-m", "PyInstaller", "--clean",
            "--distpath", str(output / "dist"), "--workpath", str(output / "work"),
            "Folimeld-desktop.spec"], cwd=root, env=environment, stdout=log,
            stderr=subprocess.STDOUT, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
