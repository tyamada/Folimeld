"""Capture build inputs and associate distribution files with that snapshot.

This captures Folimeld sources, not the corresponding sources of dependencies.
No network requests are made and no repository files are committed or published.
"""

import argparse
from datetime import datetime, timezone
import hashlib
from importlib.metadata import distributions
import json
from pathlib import Path
import platform
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit
from zipfile import ZIP_DEFLATED, ZipFile


SOURCE_DIRS = {"folimeld", "tools", "assets", "locales", "licenses", "packaging", "tests"}
ROOT_SUFFIXES = {".py", ".spec", ".sh", ".bat", ".ps1", ".md"}


def digest(path):
    checksum = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            checksum.update(chunk)
    return checksum.hexdigest()


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], stderr=subprocess.PIPE)


def source_paths(root):
    """Include tracked docs plus source inputs, including new untracked inputs."""
    if (root / ".git").exists():
        tracked = git(root, "ls-files", "-z").decode("utf-8").split("\0")
        other = git(root, "ls-files", "--others", "--exclude-standard", "-z").decode("utf-8").split("\0")
        candidates = set(tracked) | {
            name for name in other if name and (
                Path(name).parts[0] in SOURCE_DIRS or
                len(Path(name).parts) == 1 and Path(name).suffix in ROOT_SUFFIXES
            )
        }
        # Keep newly added documentation reachable from tracked Markdown, without
        # including unrelated untracked documents in the release source archive.
        pending = [name for name in candidates if name.endswith(".md")]
        seen = set()
        while pending:
            name = pending.pop()
            if name in seen or not (root / name).is_file():
                continue
            seen.add(name)
            for link in re.findall(r"\]\(([^)]+)\)", (root / name).read_text(encoding="utf-8")):
                url = urlsplit(link)
                if url.scheme or url.netloc or not url.path:
                    continue
                path = (root / name).parent / unquote(url.path)
                if not path.is_file() or not path.resolve().is_relative_to(root.resolve()):
                    continue
                relative = path.resolve().relative_to(root.resolve())
                if relative.parts[0] == "docs":
                    candidates.add(relative.as_posix())
                    if relative.suffix == ".md":
                        pending.append(relative.as_posix())
    else:
        # A source archive can be rebuilt without Git. Its manifest is the file list.
        previous = json.loads((root / "SOURCE-MANIFEST.json").read_text(encoding="utf-8"))
        candidates = set(previous["files"])
    selected = []
    for name in sorted(candidates):
        if not name:
            continue
        relative = Path(name)
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError(f"Unsafe source path: {name}")
        include = relative.parts[0] in SOURCE_DIRS | {"docs"} or (
            len(relative.parts) == 1 and (
                relative.suffix in ROOT_SUFFIXES or
                name in {"LICENSE", ".gitignore", ".gitattributes", "requirements.txt", "requirements-dev.txt"}
            )
        )
        if not include or "__pycache__" in relative.parts or relative.suffix in {".pyc", ".pyo"}:
            continue
        path = root / relative
        if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
            raise ValueError(f"Source symlinks are not supported: {name}")
        if path.is_file():
            selected.append(relative.as_posix())
    for required in ("main.py", "LICENSE", "licenses/AGPL-3.0.txt", "requirements.txt"):
        if required not in selected:
            raise ValueError(f"Required source input is missing: {required}")
    return selected


def source_datas(project_root, target):
    """Called before PyInstaller Analysis, after assets and notices are generated."""
    root = Path(project_root).resolve()
    if not re.fullmatch(r"[a-z0-9-]+", target):
        raise ValueError("Invalid build target")
    paths = source_paths(root)
    packages = sorted({(d.metadata["Name"], d.version) for d in distributions()})
    manifest = {
        "format": 1,
        "target": target,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": None,
        "working_tree_changed": None,
        "python": sys.version,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "packages": [{"name": n, "version": v} for n, v in packages],
        "files": {},
        "dependency_sources": "NOT INCLUDED: obtain matching dependency sources and review bundled native components before distribution",
    }
    if (root / ".git").exists():
        manifest["git_commit"] = git(root, "rev-parse", "HEAD").decode().strip()
        manifest["working_tree_changed"] = bool(git(root, "status", "--porcelain", "--untracked-files=normal"))
    output = root / "dist" / "source"
    output.mkdir(parents=True, exist_ok=True)
    # A unique draft prevents overwriting records from previous builds.
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    draft = output / f"Folimeld-{target}-{stamp}.zip"
    with ZipFile(draft, "x", ZIP_DEFLATED) as archive:
        for name in paths:
            data = (root / name).read_bytes()
            manifest["files"][name] = hashlib.sha256(data).hexdigest()
            archive.writestr(name, data)
        archive.writestr("SOURCE-MANIFEST.json", json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
        archive.writestr("build-requirements.txt", "".join(f"{n}=={v}\n" for n, v in packages))
        notices = root / "build" / "legal" / "Installed-packages.txt"
        if notices.exists():
            archive.write(notices, "licenses/Installed-packages.txt")
    archive_hash = digest(draft)
    archive_path = output / f"Folimeld-source-{archive_hash}.zip"
    draft.rename(archive_path)
    record = dict(manifest, source_archive=archive_path.name, source_sha256=archive_hash)
    record_path = root / "build" / "source" / target / "Build-source.txt"
    record_path.parent.mkdir(parents=True, exist_ok=True)
    record_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / f"{archive_path.stem}.json").write_text(record_path.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"Folimeld source snapshot: {archive_path}")
    return [(str(record_path), "licenses")]


def record_artifact(executable, artifact, source_dir, *, project_root=None):
    """Read the embedded record; never assign today's checkout to an old binary.

For an outer package, the caller must supply the executable actually packaged.
The package association is recorded by the build script, not inferred by hash.
"""
    from PyInstaller.archive.readers import CArchiveReader

    executable, artifact, source_dir = Path(executable), Path(artifact), Path(source_dir)
    reader = CArchiveReader(str(executable))
    key = next((k for k in reader.toc if k.replace("\\", "/") == "licenses/Build-source.txt"), None)
    if key is None:
        raise ValueError("Executable has no build source record; rebuild it instead of assigning a source snapshot retrospectively")
    record = json.loads(reader.extract(key).decode("utf-8"))
    name = record["source_archive"]
    if Path(name).name != name or not re.fullmatch(r"Folimeld-source-[0-9a-f]{64}\.zip", name):
        raise ValueError("Invalid source archive name")
    source = source_dir / name
    if digest(source) != record["source_sha256"]:
        raise ValueError("Source archive checksum mismatch")
    if project_root is not None:
        root = Path(project_root).resolve()
        if set(source_paths(root)) != set(record["files"]):
            raise ValueError("Source file list changed after snapshot; rebuild before packaging")
        for name, checksum in record["files"].items():
            if digest(root / name) != checksum:
                raise ValueError(f"Source changed after snapshot: {name}; rebuild before packaging")
    artifact_hash = digest(artifact)
    result = {
        "artifact": artifact.name,
        "artifact_sha256": artifact_hash,
        "executable": executable.name,
        "executable_sha256": digest(executable),
        "association": "embedded record" if artifact.resolve() == executable.resolve() else "packaging script supplied executable; verify package contents before publication",
        "source_archive": record["source_archive"],
        "source_sha256": record["source_sha256"],
        "git_commit": record["git_commit"],
        "working_tree_changed": record["working_tree_changed"],
        "dependency_sources": record["dependency_sources"],
    }
    destination = source_dir / f"{artifact.name}-{artifact_hash}.json"
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Artifact/source association: {destination}")
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--executable", required=True, type=Path)
    parser.add_argument("--artifact", type=Path)
    parser.add_argument("--source-dir", type=Path, default=Path("dist/source"))
    parser.add_argument("--project-root", type=Path, default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args()
    record_artifact(args.executable, args.artifact or args.executable, args.source_dir,
                    project_root=args.project_root)


if __name__ == "__main__":
    main()
