import json
from pathlib import Path
import zipfile
import pytest
from folimeld import resources
from folimeld.uv_license_info import uv_license_documents
from tools import uv_tool_build


def test_pyproject_sync_matches_repository_inputs():
    root = Path(__file__).resolve().parents[1]
    meta_x64 = uv_tool_build.validate_pyproject_sync(root, arch="x64")
    assert meta_x64["name"] == "folimeld"
    assert meta_x64["requires_python"] == ">=3.12,<3.13"
    assert len(meta_x64["dependencies"]) == 14
    assert meta_x64["dependencies"]["cryptography"] == "50.0.2"

    meta_arm64 = uv_tool_build.validate_pyproject_sync(root, arch="arm64")
    assert meta_arm64["name"] == "folimeld"
    assert len(meta_arm64["dependencies"]) == 14
    assert meta_arm64["dependencies"]["cryptography"] == "46.0.3"


def test_deterministic_wheel_build_and_embedded_resources(tmp_path, monkeypatch):
    root = Path(__file__).resolve().parents[1]
    out1 = tmp_path / "build1"
    out2 = tmp_path / "build2"
    wheel1 = uv_tool_build.build_pure_wheel(root, out1)
    wheel2 = uv_tool_build.build_pure_wheel(root, out2)
    assert wheel1.read_bytes() == wheel2.read_bytes()

    site_packages = tmp_path / "site-packages"
    with zipfile.ZipFile(wheel1, "r") as archive:
        archive.extractall(site_packages)

    extracted_res = site_packages / "folimeld" / "_resources"
    assert (extracted_res / "LICENSE").is_file()
    assert (extracted_res / "windows-uv-runtime.json").is_file()
    assert (extracted_res / "windows-arm64-uv-runtime.json").is_file()
    assert (extracted_res / "locales" / "ja.json").is_file()
    assert (extracted_res / "assets" / "Folimeld.iconset" / "icon_256x256.png").is_file()
    assert (extracted_res / "assets" / "folimeld-supporter-maid.png").is_file()
    assert (extracted_res / "documentation" / "windows-uv-licenses" / "notices.txt").is_file()
    assert (extracted_res / "documentation" / "windows-arm64-uv-licenses" / "notices.txt").is_file()

    # Verify resource_root resolves _resources when installed in site-packages
    monkeypatch.delattr(resources.sys, "_MEIPASS", raising=False)
    monkeypatch.setattr(resources, "__file__", str(site_packages / "folimeld" / "resources.py"))
    assert resources.resource_root() == extracted_res

    # Verify uv_license_documents works directly against extracted wheel _resources
    profile = json.loads((extracted_res / "windows-uv-runtime.json").read_text(encoding="utf-8"))
    monkeypatch.setattr("folimeld.uv_license_info.version", lambda name: profile["dependencies"][name])
    docs = dict(uv_license_documents(extracted_res))
    assert "Windows uv notices" in docs
    assert "Windows uv installed packages" in docs


def test_stage_release_artifacts_creates_manifest_and_checksums(tmp_path):
    root = Path(__file__).resolve().parents[1]
    stage_dir = tmp_path / "release"
    manifest = uv_tool_build.stage_release_artifacts(root, stage_dir)
    assert manifest["distribution"] == "windows-uv-tool-x64"
    assert (stage_dir / "SHA256SUMS.txt").is_file()
    assert (stage_dir / "uv-tool-release-manifest.json").is_file()
    assert (stage_dir / "Folimeld-0.3.11-windows-x64-uv-tool-source.zip").is_file()
    assert (stage_dir / "source-manifest.json").is_file()
    assert (stage_dir / "SOURCE-ASSOCIATION.txt").is_file()
    assert (stage_dir / "requirements-windows-uv.lock").is_file()
    assert (stage_dir / "THIRD-PARTY-NOTICES.txt").is_file()
    assert (stage_dir / "DEPENDENCY-SOURCES.json").is_file()
    with pytest.raises(FileExistsError):
        uv_tool_build.stage_release_artifacts(root, stage_dir)

    stage_arm64 = tmp_path / "release-arm64"
    manifest_arm64 = uv_tool_build.stage_release_artifacts(root, stage_arm64, arch="arm64")
    assert manifest_arm64["distribution"] == "windows-uv-tool-arm64"
    assert (stage_arm64 / "Folimeld-0.3.11-windows-arm64-uv-tool-source.zip").is_file()
    assert (stage_arm64 / "requirements-windows-arm64-uv.lock").is_file()
