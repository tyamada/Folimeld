"""Read-only checks for the dedicated Inno tool tree; no compilation entry point."""
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess

PRIMARY_FILES = frozenset({"ISCC.exe", "ISCmplr.dll", "ISPP.dll", "Setup.e32", "Setup.e64",
                          "SetupCustomStyle.e32", "SetupCustomStyle.e64", "SetupLdr.e32", "SetupLdr.e64"})
SETUP_POLICY = {"SetupArchitecture": "x86", "UseSetupLdr": "x86", "WizardStyle": "classic light",
                "ArchitecturesAllowed": "x64os", "ArchitecturesInstallIn64BitMode": "x64os"}
SELECTED_STUBS = ["Setup.e32", "SetupLdr.e32"]


def load_inno_manifest(root: Path):
    raw = (root / "packaging/windows/desktop-inno.json").read_bytes()
    manifest = json.loads(raw)
    profile = json.loads((root / "packaging/windows/desktop-runtime.json").read_bytes())
    if (manifest.get("schema_version") != 1 or manifest.get("distribution") != "windows-desktop-x64"
            or manifest.get("engine_version") != "7.1.1"
            or manifest.get("source_installer_sha256") != profile["inno_compiler"]["sha256"]
            or set(manifest.get("primary_files", [])) != PRIMARY_FILES
            or manifest.get("setup_policy") != SETUP_POLICY
            or manifest.get("selected_stubs") != SELECTED_STUBS
            or not PRIMARY_FILES <= manifest.get("files", {}).keys()):
        raise ValueError("Invalid Desktop Inno manifest.")
    for name, entry in manifest["files"].items():
        path = PurePosixPath(name)
        if (path.is_absolute() or ".." in path.parts or "\\" in name or ":" in name
                or path.as_posix() != name or not isinstance(entry.get("bytes"), int)
                or entry["bytes"] <= 0 or not isinstance(entry.get("sha256"), str)
                or not re.fullmatch(r"[0-9a-f]{64}", entry["sha256"])):
            raise ValueError("Unsafe or invalid Desktop Inno input.")
    return manifest, hashlib.sha256(raw).hexdigest()


def verify_setup_policy(script: Path):
    section = ""
    directives = {}
    for raw in script.read_text(encoding="utf-8-sig").splitlines():
        line = raw.strip()
        if not line or line.startswith((";", "//")):
            continue
        if re.match(r"#\s*include\b", line, re.IGNORECASE):
            raise ValueError("Inno includes require a new stub-policy review.")
        if line.startswith("[") and line.endswith("]"):
            section = line[1:-1].lower()
            continue
        if section != "setup":
            continue
        if line.startswith("#") or "=" not in line:
            raise ValueError("Inno Setup policy must use literal directives.")
        name, value = (x.strip() for x in line.split("=", 1))
        name = name.lower()
        if name in directives:
            raise ValueError("Duplicate Inno Setup directive.")
        directives[name] = value
    if (any(directives.get(k.lower()) != v for k, v in SETUP_POLICY.items())
            or "wizardstylefile" in directives or "wizardstylefiledynamicdark" in directives):
        raise ValueError("Inno stub selection no longer matches the reviewed policy.")
    return {name: directives[name.lower()] for name in SETUP_POLICY}


def _engine_version(root: Path):
    # No .iss file, stdin source, preprocessing or compilation arguments are accepted here.
    env = dict(os.environ)
    system_root = env.get("SystemRoot", "C:\\Windows")
    env["PATH"] = os.pathsep.join([str(root), str(Path(system_root) / "System32"), system_root])
    result = subprocess.run([str(root / "ISCC.exe"), "--version"], cwd=root, env=env,
                            capture_output=True, text=True, timeout=15, check=True)
    return result.stdout.strip()


def verify_inno_inputs(input_root: Path, manifest: dict, script: Path):
    policy = verify_setup_policy(script)
    root = input_root.resolve(strict=True)
    actual = set()
    for path in root.rglob("*"):
        if not path.resolve().is_relative_to(root):
            raise ValueError("Inno input escapes its dedicated directory.")
        if path.is_file():
            actual.add(path.relative_to(root).as_posix())
    if actual != set(manifest["files"]):
        raise ValueError("Missing or extra files in the pinned Inno tool tree.")
    verified = {}
    for name, expected in manifest["files"].items():
        path = root / name
        with path.open("rb") as source:
            digest = hashlib.file_digest(source, "sha256").hexdigest()
        if digest != expected["sha256"] or path.stat().st_size != expected["bytes"]:
            raise ValueError(f"Inno hash/size mismatch: {name}")
        verified[name] = digest
    version = _engine_version(root)
    if version != manifest["engine_version"]:
        raise ValueError(f"Inno engine version mismatch: {version}")
    return {"root": str(root), "engine_version": version, "files": verified,
            "setup_policy": policy, "selected_stubs": list(manifest["selected_stubs"]),
            "setup_script_sha256": hashlib.sha256(script.read_bytes()).hexdigest(), "compiled": False}
