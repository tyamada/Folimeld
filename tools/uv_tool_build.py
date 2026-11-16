"""Deterministic Pure Python wheel builder and verifier for the Windows uv tool edition."""
import argparse
import base64
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import shutil
import tomllib
import zipfile


REQUIRED_FORCE_INCLUDES = {
    "LICENSE": "folimeld/_resources/LICENSE",
    "windows-uv-runtime.json": "folimeld/_resources/windows-uv-runtime.json",
    "windows-arm64-uv-runtime.json": "folimeld/_resources/windows-arm64-uv-runtime.json",
    "locales": "folimeld/_resources/locales",
    "assets/Folimeld.iconset/icon_256x256.png": "folimeld/_resources/assets/Folimeld.iconset/icon_256x256.png",
    "assets/folimeld-supporter-maid.png": "folimeld/_resources/assets/folimeld-supporter-maid.png",
    "documentation/windows-uv-licenses": "folimeld/_resources/documentation/windows-uv-licenses",
    "documentation/windows-arm64-uv-licenses": "folimeld/_resources/documentation/windows-arm64-uv-licenses",
}

FIXED_ZIP_DATE_TIME = (2026, 1, 1, 0, 0, 0)


def _normalize_name(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def _read_app_version(root: Path) -> str:
    init_text = (root / "folimeld" / "__init__.py").read_text(encoding="utf-8")
    match = re.search(r'^__version__\s*=\s*"([A-Za-z0-9][A-Za-z0-9.+_-]*)"', init_text, re.M)
    if not match:
        raise ValueError("Unable to read __version__ from folimeld/__init__.py.")
    return match.group(1)


def validate_pyproject_sync(root: Path, arch: str = "x64") -> dict:
    """Validate pyproject.toml against runtime pins, lockfile, and app version."""
    pyproject_path = root / "pyproject.toml"
    data = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
    project = data.get("project", {})
    app_version = _read_app_version(root)
    if project.get("name") != "folimeld":
        raise ValueError("pyproject.toml project.name must be 'folimeld'.")
    if project.get("version") != app_version:
        raise ValueError("pyproject.toml version differs from folimeld/__init__.py.")
    if project.get("requires-python") != ">=3.12,<3.13":
        raise ValueError("pyproject.toml requires-python must be '>=3.12,<3.13'.")
    if project.get("gui-scripts") != {"folimeld": "folimeld.uv_tool_launcher:main"}:
        raise ValueError("Unexpected project.gui-scripts in pyproject.toml.")
    if project.get("scripts") != {"folimeld-console": "folimeld.uv_tool_launcher:main"}:
        raise ValueError("Unexpected project.scripts in pyproject.toml.")

    profile_name = "windows-arm64-uv-runtime.json" if arch == "arm64" else "windows-uv-runtime.json"
    lock_name = "requirements-windows-arm64-uv.lock" if arch == "arm64" else "requirements-windows-uv.lock"

    profile = json.loads((root / profile_name).read_text(encoding="utf-8"))
    lock_text = (root / lock_name).read_text(encoding="utf-8").replace("\r\n", "\n")
    lock_hash = hashlib.sha256(lock_text.encode("utf-8")).hexdigest()
    if lock_hash != profile.get("lock_sha256"):
        raise ValueError(f"{lock_name} hash differs from {profile_name}.")

    declared_deps = {}
    for item in project.get("dependencies", []):
        raw = item.strip()
        if ";" in raw:
            dep_part, marker = raw.split(";", 1)
            dep_part = dep_part.strip()
            marker = marker.strip()
            if arch == "arm64":
                if "platform_machine == 'ARM64'" not in marker and "platform_machine == 'aarch64'" not in marker:
                    continue
            else:
                if "platform_machine != 'ARM64'" not in marker:
                    continue
        else:
            dep_part = raw
        match = re.fullmatch(r"([A-Za-z0-9][A-Za-z0-9_.-]*)==([^\s;]+)", dep_part)
        if not match:
            raise ValueError(f"Dependency must be exact-pinned in pyproject.toml: {item}")
        name = _normalize_name(match.group(1))
        if name in declared_deps:
            raise ValueError(f"Duplicate dependency in pyproject.toml: {name}")
        declared_deps[name] = match.group(2)

    expected_deps = {_normalize_name(k): v for k, v in profile["dependencies"].items()}
    if declared_deps != expected_deps:
        raise ValueError(f"pyproject.toml dependencies differ from {profile_name}.")

    wheel_target = data.get("tool", {}).get("hatch", {}).get("build", {}).get("targets", {}).get("wheel", {})
    if wheel_target.get("packages") != ["folimeld"]:
        raise ValueError("pyproject.toml wheel target must package only ['folimeld'].")
    force_include = wheel_target.get("force-include", {})
    if force_include != REQUIRED_FORCE_INCLUDES:
        raise ValueError("pyproject.toml wheel force-include mappings differ from required resources.")

    return {
        "name": project["name"],
        "version": app_version,
        "requires_python": project["requires-python"],
        "dependencies": declared_deps,
        "lock_sha256": lock_hash,
    }


def _collect_wheel_sources(root: Path) -> list[tuple[str, Path]]:
    entries: dict[str, Path] = {}
    package_dir = root / "folimeld"
    for path in sorted(package_dir.glob("*.py")):
        entries[f"folimeld/{path.name}"] = path

    for src_rel, dst_rel in sorted(REQUIRED_FORCE_INCLUDES.items()):
        source = (root / src_rel).resolve(strict=True)
        if not source.is_relative_to(root.resolve()):
            raise ValueError(f"Unsafe resource source path: {src_rel}")
        if source.is_file():
            entries[dst_rel] = source
        elif source.is_dir():
            for child in sorted(p for p in source.rglob("*") if p.is_file()):
                rel = child.relative_to(source).as_posix()
                entries[f"{dst_rel}/{rel}"] = child
        else:
            raise FileNotFoundError(f"Missing required wheel resource: {src_rel}")
    return sorted(entries.items())


def _urlsafe_sha256(data: bytes) -> str:
    digest = hashlib.sha256(data).digest()
    return "sha256=" + base64.urlsafe_b64encode(digest).decode("ascii").rstrip("=")


def build_pure_wheel(root: Path, output_dir: Path) -> Path:
    """Build a deterministic folimeld-<version>-py3-none-any.whl archive."""
    meta = validate_pyproject_sync(root)
    version = meta["version"]
    dist_info = f"folimeld-{version}.dist-info"
    wheel_name = f"folimeld-{version}-py3-none-any.whl"
    output_dir.mkdir(parents=True, exist_ok=True)
    wheel_path = output_dir / wheel_name
    if wheel_path.exists():
        raise FileExistsError(f"Refusing to overwrite existing wheel: {wheel_path}")

    files: list[tuple[str, bytes]] = []
    for arcname, source_path in _collect_wheel_sources(root):
        files.append((arcname, source_path.read_bytes()))

    metadata_lines = [
        "Metadata-Version: 2.3",
        "Name: folimeld",
        f"Version: {version}",
        "Summary: Desktop PDF page organizer and editor",
        "Author: Takuma Yamada",
        "License-File: LICENSE",
        f"Requires-Python: {meta['requires_python']}",
        "Project-URL: Homepage, https://tyamada.github.io/Folimeld/",
        "Project-URL: Repository, https://github.com/tyamada/Folimeld",
    ]
    for dep_name, dep_ver in sorted(meta["dependencies"].items()):
        metadata_lines.append(f"Requires-Dist: {dep_name}=={dep_ver}")
    readme_text = (root / "README.md").read_text(encoding="utf-8")
    metadata_lines.extend([
        "Description-Content-Type: text/markdown",
        "",
        readme_text,
    ])
    metadata_bytes = "\n".join(metadata_lines).encode("utf-8")

    wheel_bytes = (
        "Wheel-Version: 1.0\n"
        "Generator: folimeld-uv-tool-build\n"
        "Root-Is-Purelib: true\n"
        "Tag: py3-none-any\n"
    ).encode("utf-8")

    entry_points_bytes = (
        "[console_scripts]\n"
        "folimeld-console = folimeld.uv_tool_launcher:main\n\n"
        "[gui_scripts]\n"
        "folimeld = folimeld.uv_tool_launcher:main\n"
    ).encode("utf-8")

    license_bytes = (root / "LICENSE").read_bytes()

    files.extend([
        (f"{dist_info}/licenses/LICENSE", license_bytes),
        (f"{dist_info}/METADATA", metadata_bytes),
        (f"{dist_info}/WHEEL", wheel_bytes),
        (f"{dist_info}/entry_points.txt", entry_points_bytes),
    ])

    record_buf = io.StringIO()
    writer = csv.writer(record_buf, lineterminator="\n")
    for arcname, payload in files:
        writer.writerow([arcname, _urlsafe_sha256(payload), str(len(payload))])
    record_arcname = f"{dist_info}/RECORD"
    writer.writerow([record_arcname, "", ""])
    files.append((record_arcname, record_buf.getvalue().encode("utf-8")))

    with zipfile.ZipFile(wheel_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for arcname, payload in files:
            info = zipfile.ZipInfo(arcname, date_time=FIXED_ZIP_DATE_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, payload)

    verify_wheel(wheel_path, root)
    return wheel_path


def verify_wheel(wheel_path: Path, root: Path) -> dict:
    """Verify wheel contents, embedded resources, entry points, and RECORD hashes."""
    meta = validate_pyproject_sync(root)
    version = meta["version"]
    dist_info = f"folimeld-{version}.dist-info"
    expected_sources = dict(_collect_wheel_sources(root))

    with zipfile.ZipFile(wheel_path, "r") as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise ValueError("Duplicate archive entries in wheel.")
        for name in names:
            if (name.startswith("/") or ".." in Path(name).parts
                    or "__pycache__" in name or name.endswith(".pyc")
                    or not (name.startswith("folimeld/") or name.startswith(f"{dist_info}/"))):
                raise ValueError(f"Disallowed entry in wheel: {name}")

        for arcname, source_path in expected_sources.items():
            if arcname not in names:
                raise ValueError(f"Missing expected file in wheel: {arcname}")
            if archive.read(arcname) != source_path.read_bytes():
                raise ValueError(f"Wheel file differs from source tree: {arcname}")

        extra_package_files = [
            name for name in names
            if name.startswith("folimeld/") and name not in expected_sources
        ]
        if extra_package_files:
            raise ValueError(f"Unexpected package files in wheel: {extra_package_files}")

        entry_points_text = archive.read(f"{dist_info}/entry_points.txt").decode("utf-8")
        if ("folimeld = folimeld.uv_tool_launcher:main" not in entry_points_text
                or "folimeld-console = folimeld.uv_tool_launcher:main" not in entry_points_text):
            raise ValueError("Missing required entry points in wheel.")

        record_name = f"{dist_info}/RECORD"
        record_text = archive.read(record_name).decode("utf-8")
        rows = list(csv.reader(io.StringIO(record_text)))
        recorded = {}
        for row in rows:
            if len(row) != 3:
                raise ValueError("Invalid RECORD line in wheel.")
            rec_path, rec_hash, rec_size = row
            recorded[rec_path] = (rec_hash, rec_size)
            if rec_path == record_name:
                if rec_hash or rec_size:
                    raise ValueError("RECORD entry for itself must have empty hash and size.")
            else:
                payload = archive.read(rec_path)
                if rec_hash != _urlsafe_sha256(payload) or rec_size != str(len(payload)):
                    raise ValueError(f"RECORD mismatch for {rec_path}")
        if set(recorded) != set(names):
            raise ValueError("RECORD file list does not match wheel archive members.")

    wheel_bytes = wheel_path.read_bytes()
    return {
        "wheel": wheel_path.name,
        "version": version,
        "sha256": hashlib.sha256(wheel_bytes).hexdigest(),
        "bytes": len(wheel_bytes),
        "file_count": len(names),
    }


UV_TOOL_OWNED_PATHS = {
    "CHANGELOG.md",
    "CHANGELOG_ja.md",
    "README.md",
    "README_ja.md",
    "documentation/windows-uv-tool.md",
    "documentation/windows-uv-tool_ja.md",
    "folimeld/app.py",
    "folimeld/desktop_profile.py",
    "folimeld/distribution.py",
    "folimeld/i18n.py",
    "folimeld/license_info.py",
    "folimeld/resources.py",
    "folimeld/source_profile.py",
    "folimeld/support_dialog.py",
    "folimeld/uv_license_info.py",
    "folimeld/uv_tool_launcher.py",
    "folimeld/uv_tool_profile.py",
    "install_uv.ps1",
    "launch_uv.py",
    "pyproject.toml",
    "requirements-windows-arm64-uv.lock",
    "windows-arm64-uv-runtime.json",
    "packaging/windows/desktop-arm64-runtime.json",
    "packaging/windows/desktop-arm64-runtime-requirements.txt",
    "packaging/windows/desktop-arm64-tools-requirements.txt",
    "packaging/windows/desktop-arm64-crt.json",
    "packaging/windows/desktop-arm64-inno.json",
    "packaging/windows/Folimeld-desktop-arm64.iss",
    "tests/test_desktop_profile.py",
    "tests/test_distribution.py",
    "tests/test_image_import.py",
    "tests/test_uv_tool_build.py",
    "tests/test_uv_tool_launcher.py",
    "tests/test_uv_tool_profile.py",
    "tools/desktop_build.py",
    "tools/desktop_compile.py",
    "tools/desktop_crt.py",
    "tools/desktop_inno.py",
    "tools/desktop_runtime_terms.py",
    "tools/source_bundle.py",
    "tools/uv_tool_build.py",
}


def build_source_archive(
    root: Path, output_dir: Path, version: str, arch: str = "x64"
) -> tuple[Path, Path, str | None]:
    """Build a deterministic corresponding source ZIP and source-manifest.json."""
    from tools.source_bundle import DOCUMENTATION_DIR, ROOT_CONFIG_FILES, ROOT_SUFFIXES, SOURCE_DIRS, git, source_paths

    git_commit = None
    dirty_non_uv: set[str] = set()
    if (root / ".git").exists():
        git_commit = git(root, "rev-parse", "HEAD").decode("utf-8").strip()
        tracked_head = set(
            git(root, "ls-tree", "-r", "--name-only", "-z", "HEAD").decode("utf-8").split("\0")
        ) - {""}
        changed_from_head = set(
            git(root, "diff", "--name-only", "-z", "HEAD").decode("utf-8").split("\0")
        ) - {""}
        dirty_non_uv = changed_from_head - UV_TOOL_OWNED_PATHS
        candidates = tracked_head | UV_TOOL_OWNED_PATHS
        paths = []
        for name in sorted(candidates):
            rel = Path(name)
            include = rel.parts[0] in SOURCE_DIRS | {DOCUMENTATION_DIR} or (
                len(rel.parts) == 1 and (
                    rel.suffix in ROOT_SUFFIXES
                    or name in {"LICENSE", ".gitignore", ".gitattributes", "requirements.txt", "requirements-dev.txt"}
                    | ROOT_CONFIG_FILES
                )
            )
            if include and (root / rel).is_file():
                paths.append(rel.as_posix())
    else:
        paths = sorted(set(source_paths(root)) | {
            "pyproject.toml",
            "documentation/windows-uv-tool_ja.md",
            "documentation/windows-uv-tool.md",
        })

    file_payloads: dict[str, bytes] = {}
    files_manifest: dict[str, str] = {}
    for rel in paths:
        if rel in dirty_non_uv:
            payload = git(root, "show", f"HEAD:{rel}")
        else:
            path = (root / rel).resolve(strict=True)
            if not path.is_relative_to(root.resolve()) or not path.is_file():
                raise ValueError(f"Invalid source archive member: {rel}")
            payload = path.read_bytes()
        file_payloads[rel] = payload
        files_manifest[rel] = hashlib.sha256(payload).hexdigest()

    manifest_data = {
        "schema_version": 1,
        "distribution": f"windows-uv-tool-{arch}",
        "version": version,
        "git_commit": git_commit,
        "files": files_manifest,
    }
    manifest_bytes = (json.dumps(manifest_data, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    manifest_path = output_dir / "source-manifest.json"
    manifest_path.write_bytes(manifest_bytes)

    zip_path = output_dir / f"Folimeld-{version}-windows-{arch}-uv-tool-source.zip"
    if zip_path.exists():
        raise FileExistsError(f"Refusing to overwrite existing source archive: {zip_path}")

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for rel in paths:
            payload = file_payloads[rel]
            info = zipfile.ZipInfo(rel, date_time=FIXED_ZIP_DATE_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, payload)
        info = zipfile.ZipInfo("SOURCE-MANIFEST.json", date_time=FIXED_ZIP_DATE_TIME)
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o644 << 16
        archive.writestr(info, manifest_bytes)

    return zip_path, manifest_path, git_commit


def stage_release_artifacts(root: Path, output_dir: Path, arch: str = "x64") -> dict:
    """Build the verified wheel and stage companion release files and SHA256SUMS.txt."""
    if output_dir.exists():
        raise FileExistsError(f"Output directory already exists: {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=False)
    wheel_path = build_pure_wheel(root, output_dir)
    wheel_info = verify_wheel(wheel_path, root)
    source_zip_path, source_manifest_path, git_commit = build_source_archive(
        root, output_dir, wheel_info["version"], arch=arch
    )
    source_zip_sha256 = hashlib.sha256(source_zip_path.read_bytes()).hexdigest()
    source_manifest_sha256 = hashlib.sha256(source_manifest_path.read_bytes()).hexdigest()

    association_lines = [
        f"distribution: windows-uv-tool-{arch}",
        f"version: {wheel_info['version']}",
        f"git_commit: {git_commit or 'none'}",
        f"wheel: {wheel_path.name}",
        f"wheel_sha256: {wheel_info['sha256']}",
        f"source_archive: {source_zip_path.name}",
        f"source_archive_sha256: {source_zip_sha256}",
        f"source_manifest: {source_manifest_path.name}",
        f"source_manifest_sha256: {source_manifest_sha256}",
    ]
    association_path = output_dir / "SOURCE-ASSOCIATION.txt"
    association_path.write_text("\n".join(association_lines) + "\n", encoding="utf-8")

    lock_file = "requirements-windows-arm64-uv.lock" if arch == "arm64" else "requirements-windows-uv.lock"
    runtime_file = "windows-arm64-uv-runtime.json" if arch == "arm64" else "windows-uv-runtime.json"
    lic_dir = "windows-arm64-uv-licenses" if arch == "arm64" else "windows-uv-licenses"

    companions = {
        lock_file: root / lock_file,
        runtime_file: root / runtime_file,
        "THIRD-PARTY-NOTICES.txt": root / "documentation" / lic_dir / "notices.txt",
        "DEPENDENCY-SOURCES.json": root / "documentation" / lic_dir / "sources.json",
    }
    artifacts = {
        wheel_path.name: {
            "sha256": wheel_info["sha256"],
            "bytes": wheel_info["bytes"],
        },
        source_zip_path.name: {
            "sha256": source_zip_sha256,
            "bytes": source_zip_path.stat().st_size,
        },
        source_manifest_path.name: {
            "sha256": source_manifest_sha256,
            "bytes": source_manifest_path.stat().st_size,
        },
        association_path.name: {
            "sha256": hashlib.sha256(association_path.read_bytes()).hexdigest(),
            "bytes": association_path.stat().st_size,
        },
    }
    for target_name, src_path in companions.items():
        dst_path = output_dir / target_name
        shutil.copyfile(src_path, dst_path)
        raw = dst_path.read_bytes()
        artifacts[target_name] = {
            "sha256": hashlib.sha256(raw).hexdigest(),
            "bytes": len(raw),
        }

    sums_lines = [
        f"{info['sha256']}  {name}"
        for name, info in sorted(artifacts.items())
    ]
    sums_path = output_dir / "SHA256SUMS.txt"
    sums_path.write_text("\n".join(sums_lines) + "\n", encoding="utf-8")

    manifest = {
        "schema_version": 1,
        "distribution": f"windows-uv-tool-{arch}",
        "version": wheel_info["version"],
        "requires_python": ">=3.12,<3.13",
        "artifacts": artifacts,
    }
    (output_dir / "uv-tool-release-manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--arch", choices=["x64", "arm64"], default="x64")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    stage_release_artifacts(root, args.output.resolve(), arch=args.arch)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
