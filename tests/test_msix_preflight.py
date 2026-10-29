from io import BytesIO
import json
from pathlib import Path
import shutil
import struct
import subprocess
import sys
from zipfile import ZipFile

from PIL import Image
import pytest

from tools.msix_preflight import (compare_previous, inspect_package, main, render_manifest,
                                  validate_config, version_tuple)


@pytest.fixture
def config():
    return {
        'identity_name': '12345.ExampleFolimeld', 'publisher': 'CN=12345678-1234-1234-1234-123456789abc',
        'publisher_display_name': 'Example & Co', 'package_version': '1.0.0.0',
        'minimum_windows_version': '10.0.22000.0', 'maximum_tested_windows_version': '10.0.26100.0',
        'channel': 'store', 'architecture': 'x64',
    }


def make_package(path, config, *, missing=None, machine=None, manifest=None):
    with ZipFile(path, 'w') as archive:
        archive.writestr('AppxManifest.xml', manifest or render_manifest(config))
        archive.writestr('LICENSE.txt', 'Test license')
        executable = bytearray(134)
        executable[:2] = b'MZ'
        struct.pack_into('<I', executable, 60, 128)
        executable[128:132] = b'PE\0\0'
        struct.pack_into('<H', executable, 132, machine or {'x64': 0x8664, 'arm64': 0xAA64}[config['architecture']])
        archive.writestr('Folimeld.exe', executable)
        for name, size in {'StoreLogo': (50, 50), 'Square44x44Logo': (44, 44),
                           'Square150x150Logo': (150, 150), 'Square71x71Logo': (71, 71),
                           'Wide310x150Logo': (310, 150), 'Square310x310Logo': (310, 310)}.items():
            if name == missing:
                continue
            stream = BytesIO()
            Image.new('RGB', size).save(stream, format='PNG')
            archive.writestr(f'Assets/{name}.png', stream.getvalue())
    return path


@pytest.mark.parametrize('version', ['0.3.3.0', '1.0.0.1', '1.0.65536.0', '1.0.0', '1.0.0.0.1', '01.0.0.0', '-1.0.0.0'])
def test_store_rejects_invalid_version(config, version):
    with pytest.raises(ValueError):
        validate_config({**config, 'package_version': version})


@pytest.mark.parametrize('values', [
    {'identity_name': 'Folimeld.Dev'}, {'identity_name': ''}, {'publisher': 'CN=REPLACE'},
    {'publisher': ''}, {'publisher_display_name': ' '}, {'minimum_windows_version': '10.0.17763.0'},
    {'maximum_tested_windows_version': '10.0.19041.0'}, {'architecture': 'x86'},
])
def test_store_rejects_development_or_incomplete_settings(config, values):
    with pytest.raises(ValueError):
        validate_config({**config, **values})


@pytest.mark.parametrize('architecture', ['x64', 'arm64'])
def test_package_static_checks(config, tmp_path, architecture):
    config['architecture'] = architecture
    path = make_package(tmp_path / 'app.msix', config)
    result = inspect_package(path, validate_config(config))
    assert result['static_checks_passed']
    assert result['identity']['ProcessorArchitecture'] == architecture
    assert 'Partner Center validation' in result['requires']
    assert len(result['sha256']) == 64


def test_package_rejects_wrong_identity_architecture_and_missing_asset(config, tmp_path):
    path = make_package(tmp_path / 'app.msix', config)
    with pytest.raises(ValueError, match='configuration'):
        inspect_package(path, {**config, 'identity_name': 'Other.App'})
    path = make_package(path, config, machine=0xAA64)
    with pytest.raises(ValueError, match='architecture'):
        inspect_package(path, config)
    path = make_package(path, config, missing='StoreLogo')
    with pytest.raises(KeyError):
        inspect_package(path, config)
    path = make_package(path, config, manifest=render_manifest(config).replace('Assets\\StoreLogo.png', '..\\StoreLogo.png'))
    with pytest.raises(ValueError, match='logo'):
        inspect_package(path, config)


def test_package_version_must_increase_within_same_family(config, tmp_path):
    path = make_package(tmp_path / 'old.msix', config)
    with pytest.raises(ValueError, match='greater'):
        compare_previous(config, path)
    compare_previous({**config, 'package_version': '1.0.1.0'}, path)
    with pytest.raises(ValueError, match='family'):
        compare_previous({**config, 'publisher': 'CN=Other'}, path)


def test_cli_requires_store_config_and_writes_no_false_success(tmp_path, monkeypatch):
    monkeypatch.setattr(sys, 'argv', ['msix_preflight', 'prepare', '--store', '--output-directory', str(tmp_path)])
    with pytest.raises(SystemExit) as error:
        main()
    assert error.value.code == 1
    assert not (tmp_path / 'config.json').exists()
    assert version_tuple('65535.65535.65535.0') == (65535, 65535, 65535, 0)


def test_cli_rejects_blank_example_and_stale_check_report(tmp_path, monkeypatch, config):
    profile = tmp_path / 'profile.json'
    profile.write_text(json.dumps({k: v for k, v in config.items() if k not in ('channel', 'architecture')}))
    (tmp_path / 'preflight.json').write_text('{"static_checks_passed": true}')
    monkeypatch.setattr(sys, 'argv', ['msix_preflight', 'check', '--store', '--store-config', str(profile),
                                   '--package', str(tmp_path / 'missing.msix'), '--output-directory', str(tmp_path)])
    with pytest.raises(SystemExit):
        main()
    assert not (tmp_path / 'preflight.json').exists()


@pytest.mark.skipif(sys.platform != 'win32', reason='Windows PowerShell build entry point')
def test_powershell_validate_only_and_store_failure_before_build(tmp_path, config):
    root = Path(__file__).resolve().parent.parent
    command = [shutil.which('powershell.exe'), '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File',
               str(root / 'build_msix.ps1'), '-ValidateOnly', '-PythonExecutable', sys.executable]
    valid = subprocess.run(command, capture_output=True, text=True)
    assert valid.returncode == 0, valid.stderr
    invalid = subprocess.run([*command, '-Store'], capture_output=True, text=True)
    assert invalid.returncode != 0 and 'StoreConfig' in invalid.stderr
    profile = tmp_path / 'profile.json'
    profile.write_text(json.dumps({k: v for k, v in config.items() if k not in ('channel', 'architecture')}))
    valid = subprocess.run([*command, '-Store', '-StoreConfig', str(profile)], capture_output=True, text=True)
    assert valid.returncode == 0, valid.stderr
    invalid = subprocess.run([*command, '-Store', '-StoreConfig', str(profile), '-PackageVersion', '2.0.0.0'],
                             capture_output=True, text=True)
    assert invalid.returncode != 0 and 'configuration' not in invalid.stdout
