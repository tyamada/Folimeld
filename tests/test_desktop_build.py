import hashlib
import json
import pytest
from tools.desktop_build import reviewed_legal_datas


def legal(root, extra=None):
    files = {}
    for name in ["Installed-packages.txt", "THIRD-PARTY-NOTICES.txt", "DEPENDENCY-SOURCES.json"]:
        (root / name).write_text("example")
        files[name] = hashlib.sha256(b"example").hexdigest()
    if extra: files.update(extra)
    (root / "reviewed-files.json").write_text(json.dumps({"distribution": "windows-desktop-x64", "files": files}))


def test_reviewed_legal_inputs_are_exact(tmp_path):
    legal(tmp_path)
    assert len(reviewed_legal_datas(tmp_path)) == 3
    (tmp_path / "THIRD-PARTY-NOTICES.txt").write_text("changed")
    with pytest.raises(ValueError, match="hash mismatch"): reviewed_legal_datas(tmp_path)


def test_legal_inputs_cannot_escape_root(tmp_path):
    legal(tmp_path, {"../outside": "0" * 64})
    with pytest.raises(ValueError, match="Unsafe"): reviewed_legal_datas(tmp_path)


def test_missing_desktop_specific_legal_records_stop_build(tmp_path):
    (tmp_path / "reviewed-files.json").write_text(json.dumps({"distribution": "windows-uv", "files": {}}))
    with pytest.raises(ValueError, match="Desktop-specific"): reviewed_legal_datas(tmp_path)


def test_desktop_inputs_are_independent(tmp_path):
    from tools.desktop_build import load_desktop_inputs
    from pathlib import Path
    import shutil
    target = tmp_path / "packaging/windows"
    target.mkdir(parents=True)
    for filename in ("desktop-runtime.json", "desktop-runtime-requirements.txt", "desktop-tools-requirements.txt"):
        shutil.copyfile(Path(__file__).resolve().parents[1] / "packaging/windows" / filename, target / filename)
    (tmp_path / "windows-uv-runtime.json").write_text("invalid and discontinued")
    profile, pins, digest = load_desktop_inputs(tmp_path)
    assert len(profile["dependencies"]) == 14
    assert pins["pyinstaller"] == "6.22.2"
    assert len(digest) == 64
    data = json.loads((target / "desktop-runtime.json").read_text())
    data["wheels"]["pillow"]["sha256"] = "bad"
    (target / "desktop-runtime.json").write_text(json.dumps(data))
    with pytest.raises(ValueError, match="Invalid Desktop wheel"):
        load_desktop_inputs(tmp_path)


def test_archive_gate_checks_contents_and_containment(tmp_path):
    from tools.desktop_build import verify_desktop_archives
    entry = {"filename": "input.whl", "sha256": hashlib.sha256(b"verified").hexdigest(), "bytes": 8}
    profile = {"python": dict(entry, archive="input.whl"), "wheels": {},
               "tool_wheels": {}, "inno_compiler": entry}
    (tmp_path / "input.whl").write_bytes(b"verified")
    assert verify_desktop_archives(profile, tmp_path) == {"input.whl": entry["sha256"]}
    (tmp_path / "input.whl").write_bytes(b"tampered")
    with pytest.raises(ValueError, match="hash mismatch"):
        verify_desktop_archives(profile, tmp_path)
    profile["python"]["archive"] = "../outside.whl"
    (tmp_path.parent / "outside.whl").write_bytes(b"verified")
    with pytest.raises(ValueError, match="Unsafe"):
        verify_desktop_archives(profile, tmp_path)


@pytest.fixture
def desktop_inputs(tmp_path):
    from pathlib import Path
    import shutil
    root = Path(__file__).resolve().parents[1] / "packaging/windows"
    target = tmp_path / "packaging/windows"
    target.mkdir(parents=True)
    for filename in ("desktop-runtime.json", "desktop-runtime-requirements.txt", "desktop-tools-requirements.txt"):
        shutil.copyfile(root / filename, target / filename)
    return tmp_path


@pytest.mark.parametrize("section,name", [("wheels", "pillow"), ("tool_wheels", "pefile")])
@pytest.mark.parametrize("field,value", [
    ("sha256", "z" * 64), ("sha256", "f" * 63), ("sha256", "F" * 64), ("sha256", None),
    ("url", "http://files.pythonhosted.org/packages/{filename}"),
    ("url", "https://files.pythonhosted.org.evil.invalid/packages/{filename}"),
    ("url", "https://files.pythonhosted.org@evil.invalid/packages/{filename}"),
    ("url", "https://user@files.pythonhosted.org/packages/{filename}"),
    ("url", "https://files.pythonhosted.org:443/packages/{filename}"),
    ("url", "https://files.pythonhosted.org/packages/other.whl"),
    ("url", "https://files.pythonhosted.org/packages/{filename}?extra=1"),
    ("url", "https://files.pythonhosted.org/packages/{filename}#fragment"),
    ("url", "https://files.pythonhosted.org/packages/%2e%2e/{filename}"),
    ("url", "https://files.pythonhosted.org/packages/\n{filename}"),
    ("url", "https://files.pythonhosted.org/packages/%0a/{filename}"),
    ("url", "https://files.pythonhosted.org/packages/%7f/{filename}"),
    ("filename", "../other.whl"),
])
def test_bad_wheel_format_stops_manifest_load(desktop_inputs, section, name, field, value):
    from tools.desktop_build import load_desktop_inputs
    path = desktop_inputs / "packaging/windows/desktop-runtime.json"
    profile = json.loads(path.read_text())
    wheel = profile[section][name]
    wheel[field] = value.format(filename=wheel["filename"]) if isinstance(value, str) else value
    path.write_text(json.dumps(profile))
    with pytest.raises(ValueError, match="Invalid Desktop (tool|wheel) input"):
        load_desktop_inputs(desktop_inputs)


@pytest.mark.parametrize("filename", ["desktop-runtime-requirements.txt", "desktop-tools-requirements.txt"])
@pytest.mark.parametrize("change", ["missing", "duplicate", "hash", "url", "extra", "option", "flag", "duplicate-flag", "version-only"])
def test_requirements_must_match_json(desktop_inputs, filename, change):
    from tools.desktop_build import load_desktop_inputs
    path = desktop_inputs / "packaging/windows" / filename
    lines = path.read_text().splitlines()
    index = next(i for i, line in enumerate(lines) if " @ " in line)
    if change == "missing":
        lines.pop(index)
    elif change == "duplicate":
        lines.append(lines[index].split(" @ ")[0].upper() + " @ " + lines[index].split(" @ ", 1)[1])
    elif change == "hash":
        lines[index] = lines[index].split("--hash=sha256:")[0] + "--hash=sha256:" + "0" * 64
    elif change == "url":
        lines[index] = lines[index].replace("/packages/", "/packages/changed/")
    elif change == "extra":
        lines.append("unexpected @ https://files.pythonhosted.org/packages/a.whl --hash=sha256:" + "0" * 64)
    elif change == "option":
        lines.append("--extra-index-url https://example.invalid")
    elif change == "flag":
        lines.remove("--require-hashes")
    elif change == "duplicate-flag":
        lines.append("--require-hashes")
    elif change == "version-only":
        lines[index] = lines[index].split(" @ ")[0] + "==1.0"
    path.write_text("\n".join(lines) + "\n")
    with pytest.raises(ValueError, match="Desktop requirement"):
        load_desktop_inputs(desktop_inputs)


def test_requirements_hashes_and_comments(desktop_inputs):
    from tools.desktop_build import load_desktop_inputs, verify_desktop_requirements
    profile, pins, digest = load_desktop_inputs(desktop_inputs)
    hashes = verify_desktop_requirements(desktop_inputs, profile)
    assert len(hashes) == 2
    path = desktop_inputs / "packaging/windows/desktop-tools-requirements.txt"
    assert hashes[path.name] == hashlib.sha256(path.read_bytes()).hexdigest()
    path.write_text("# additional review note\n" + path.read_text())
    assert verify_desktop_requirements(desktop_inputs, profile)[path.name] != hashes[path.name]
