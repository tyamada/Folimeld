"""Reviewed Desktop installer entry. Default is verification only; no auto-approval."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import struct
import subprocess
import sys

from tools.desktop_build import reviewed_legal_datas
from tools.desktop_crt import load_crt_manifest, verify_collected_crt
from tools.desktop_inno import load_inno_manifest, verify_inno_inputs


def _sha(path):
    with path.open("rb") as source:
        return hashlib.file_digest(source, "sha256").hexdigest()


def _relative(name):
    if not isinstance(name, str):
        raise ValueError("Invalid reviewed path.")
    path = PurePosixPath(name)
    if (not name or name == "." or path.is_absolute() or ".." in path.parts
            or "\\" in name or ":" in name or path.as_posix() != name):
        raise ValueError("Unsafe reviewed path.")
    return name


def _digest(value):
    if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
        raise ValueError("Invalid reviewed SHA-256.")
    return value


def _tree(root):
    result = {}
    for path in root.rglob("*"):
        if path.is_symlink() or path.is_junction() or not path.resolve().is_relative_to(root):
            raise ValueError("Linked or escaping payload input.")
        if path.is_file():
            result[path.relative_to(root).as_posix()] = _sha(path)
    return result


def _safe_argument(path):
    text = str(path)
    if any(c in text for c in '\r\n"') or any(ord(c) < 32 for c in text):
        raise ValueError("Unsafe compiler path argument.")
    return text


def _disjoint(a, b):
    return not (a.is_relative_to(b) or b.is_relative_to(a))


def _x86_or_x64(path, machine):
    with path.open("rb") as source:
        header = source.read(64)
        if len(header) != 64 or header[:2] != b"MZ":
            raise ValueError("Invalid reviewed executable PE.")
        source.seek(struct.unpack_from("<I", header, 0x3c)[0])
        if source.read(6) != b"PE\0\0" + struct.pack("<H", machine):
            raise ValueError("Unexpected executable architecture.")


def verify_compile_inputs(repo, *, payload_root, payload_review, legal_root, inno_root,
                          output, version, output_created=False):
    if (not re.fullmatch(r"[0-9]+(?:\.[0-9]+){3}", version)
            or any(int(x) > 65535 for x in version.split("."))):
        raise ValueError("Use a four-part numeric Desktop version.")
    payload = payload_root.resolve(strict=True)
    legal = legal_root.resolve(strict=True)
    inno = inno_root.resolve(strict=True)
    review_path = payload_review.resolve(strict=True)
    destination = output.resolve()
    for path in (payload, legal, inno, review_path, destination):
        _safe_argument(path)
    if (not payload.is_dir() or not legal.is_dir() or not inno.is_dir()
            or not all(_disjoint(destination, x) for x in (payload, legal, inno, repo.resolve()))
            or not all(_disjoint(a, b) for a, b in ((payload, legal), (payload, inno), (legal, inno)))
            or review_path.is_relative_to(payload) or review_path.is_relative_to(destination)):
        raise ValueError("Compile output must be separate from inputs and repository.")
    if not output_created and destination.exists():
        raise FileExistsError("Use a new installer output directory.")
    if output_created and (not destination.is_dir() or output.is_symlink() or output.is_junction()):
        raise ValueError("Installer output directory changed.")
    # Never create review records. Their contents must come from an actual review.
    review = json.loads(review_path.read_bytes())
    if (review.get("schema_version") != 1 or review.get("distribution") != "windows-desktop-x64"
            or review.get("status") != "reviewed-for-desktop-compile" or review.get("version") != version):
        raise ValueError("An explicit matching Desktop payload review is required.")
    reviewed_legal_datas(legal)
    legal_manifest = legal / "reviewed-files.json"
    bindings = {"legal_manifest_sha256": _sha(legal_manifest),
                "inno_manifest_sha256": _sha(repo / "packaging/windows/desktop-inno.json"),
                "crt_manifest_sha256": _sha(repo / "packaging/windows/desktop-crt.json"),
                "runtime_manifest_sha256": _sha(repo / "packaging/windows/desktop-runtime.json"),
                "setup_script_sha256": _sha(repo / "packaging/windows/Folimeld-desktop.iss")}
    for name, actual in bindings.items():
        if _digest(review.get(name)) != actual:
            raise ValueError(f"Reviewed binding changed: {name}")
    expected = {_relative(name): _digest(value) for name, value in review.get("files", {}).items()}
    actual = _tree(payload)
    if not expected or actual != expected:
        raise ValueError("Payload file set or hash differs from its reviewed ledger.")
    required = {"FolimeldDesktop.exe", "_internal/python312.dll", "_internal/LICENSE"}
    if not required <= actual.keys() or actual["_internal/LICENSE"] != _sha(repo / "LICENSE"):
        raise ValueError("Missing Desktop runtime or application license.")
    _x86_or_x64(payload / "FolimeldDesktop.exe", 0x8664)
    legal_files = json.loads(legal_manifest.read_bytes())["files"]
    packaged_legal = {"_internal/licenses/" + _relative(name): _digest(value)
                      for name, value in legal_files.items()}
    if {name: value for name, value in actual.items() if name.startswith("_internal/licenses/")} != packaged_legal:
        raise ValueError("Packaged legal files do not match reviewed legal inputs.")
    crt_manifest, _ = load_crt_manifest(repo)
    crt = verify_collected_crt(payload, crt_manifest)
    # Hash payload/legal inputs before any tool process, and recheck the whole tool tree.
    inno_manifest, _ = load_inno_manifest(repo)
    tools = verify_inno_inputs(inno, inno_manifest, repo / "packaging/windows/Folimeld-desktop.iss")
    return {"version": version, "payload_root": str(payload), "legal_root": str(legal),
            "inno_root": str(inno), "output": str(destination), "bindings": bindings,
            "payload_review_sha256": _sha(review_path), "payload_files": actual,
            "crt": crt, "inno": tools}


def compiler_command(repo, state):
    return [str(Path(state["inno_root"]) / "ISCC.exe"), "--no-ide-signtools",
            "--define=DesktopVersion=" + state["version"],
            "--define=PayloadRoot=" + _safe_argument(state["payload_root"]),
            "--define=OutputRoot=" + _safe_argument(state["output"]),
            "--define=PayloadReviewed=1", str(repo / "packaging/windows/Folimeld-desktop.iss")]


def compile_reviewed(repo, **inputs):
    before = verify_compile_inputs(repo, **inputs)
    destination = Path(before["output"])
    destination.mkdir()  # No reuse or overwrite; parent must already exist.
    attempted = False
    try:
        with (destination / "compile-inputs.json").open("x", encoding="utf-8") as f:
            json.dump(before, f, indent=2)
        with (destination / "iscc.log").open("x", encoding="utf-8") as log:
            # The final input operation before starting ISCC is a complete recheck.
            current = verify_compile_inputs(repo, output_created=True, **inputs)
            if current != before:
                raise ValueError("Compile inputs changed after preflight.")
            system_root = os.environ.get("SystemRoot", "C:\\Windows")
            env = {name: value for name, value in os.environ.items()
                   if name.upper() in {"SYSTEMROOT", "WINDIR", "TEMP", "TMP", "USERPROFILE",
                                       "LOCALAPPDATA", "APPDATA", "PROGRAMDATA", "COMSPEC"}}
            env["PATH"] = os.pathsep.join([before["inno_root"], str(Path(system_root) / "System32"), system_root])
            attempted = True
            result = subprocess.run(compiler_command(repo, before), cwd=before["inno_root"], env=env,
                                    stdin=subprocess.DEVNULL, stdout=log, stderr=subprocess.STDOUT)
        if result.returncode:
            raise RuntimeError(f"ISCC failed with exit code {result.returncode}.")
        after = verify_compile_inputs(repo, output_created=True, **inputs)
        if after != before:
            raise ValueError("Compile inputs changed during ISCC execution.")
        installer = destination / ("Folimeld-Desktop-" + before["version"] + "-x64-setup.exe")
        if not installer.is_file() or installer.is_symlink() or not installer.resolve().is_relative_to(destination):
            raise ValueError("Expected installer is missing or linked.")
        if {p.name for p in destination.iterdir()} != {"compile-inputs.json", "iscc.log", installer.name}:
            raise ValueError("Unexpected compiler outputs.")
        _x86_or_x64(installer, 0x14c)
        record = {"status": "compiled-not-release-approved", "installer": installer.name,
                  "bytes": installer.stat().st_size, "sha256": _sha(installer),
                  "selected_stubs": before["inno"]["selected_stubs"]}
    except Exception as error:
        record = {"status": "failed-not-approved", "compiler_attempted": attempted, "error": str(error)}
        with (destination / "compile-result.json").open("x", encoding="utf-8") as f:
            json.dump(record, f, indent=2)
        raise
    with (destination / "compile-result.json").open("x", encoding="utf-8") as f:
        json.dump(record, f, indent=2)
    return record


def main():
    parser = argparse.ArgumentParser(description="Verify reviewed Desktop inputs; compile only with --compile.")
    for name in ("payload-root", "payload-review", "legal-root", "inno-root", "output"):
        parser.add_argument("--" + name, type=Path, required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--compile", action="store_true")
    args = vars(parser.parse_args())
    compile_requested = args.pop("compile")
    repo = Path(__file__).resolve().parents[1]
    if compile_requested and (sys.platform != "win32" or struct.calcsize("P") != 8):
        parser.error("Compile only on Windows x64.")
    result = compile_reviewed(repo, **args) if compile_requested else verify_compile_inputs(repo, **args)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
