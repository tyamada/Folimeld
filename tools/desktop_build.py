"""Desktop build preflight. No compiler runs without explicitly calling main."""
import argparse
import hashlib
from importlib.metadata import version
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import struct

from tools.windows_build_environment import build_environment
from tools.desktop_crt import load_crt_manifest, verify_crt_inputs


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
        wheel = profile["wheels"][name]
        if (wheel["version"] != pin or len(wheel["sha256"]) != 64
                or any(c not in "0123456789abcdef" for c in wheel["sha256"])
                or not wheel["url"].startswith("https://files.pythonhosted.org/")):
            raise ValueError(f"Invalid Desktop wheel input: {name}")
    pins = dict(profile["dependencies"], **profile["build_tools"])
    return profile, pins, hashlib.sha256(data).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--legal-root", type=Path, required=True)
    parser.add_argument("--version-info", type=Path, required=True)
    parser.add_argument("--crt-root", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    if (sys.platform != "win32" or struct.calcsize("P") != 8
            or platform.machine().lower() not in {"amd64", "x86_64"}):
        raise RuntimeError("Build on Windows x64.")
    profile, pins, profile_hash = load_desktop_inputs(root)
    if platform.python_version() != profile["python"]["version"]:
        raise RuntimeError("Desktop build requires CPython 3.12.16.")
    for name, pin in pins.items():
        if version(name) != pin:
            raise RuntimeError(f"Build dependency drift: {name}")
    crt_manifest, crt_manifest_hash = load_crt_manifest(root)
    crt_inputs = verify_crt_inputs(args.crt_root, crt_manifest)
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
        "crt_manifest_sha256": crt_manifest_hash, "crt_inputs": crt_inputs, "legal_root": str(args.legal_root.resolve()),
        "version_info_sha256": hashlib.sha256(args.version_info.read_bytes()).hexdigest()}, indent=2), encoding="utf-8")
    with (output / "pyinstaller.log").open("w", encoding="utf-8") as log:
        return subprocess.run([sys.executable, "-m", "PyInstaller", "--clean",
            "--distpath", str(output / "dist"), "--workpath", str(output / "work"),
            "Folimeld-desktop.spec"], cwd=root, env=environment, stdout=log,
            stderr=subprocess.STDOUT, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
