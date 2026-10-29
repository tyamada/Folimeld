from pathlib import Path
import subprocess
import sys
from zipfile import ZipFile

import pytest


pytestmark = pytest.mark.skipif(sys.platform != 'win32', reason='Windows PowerShell packaging helpers')
ROOT = Path(__file__).resolve().parents[1]
PREPARE = ROOT / 'tools/prepare_msix_test.ps1'


def run_prepare(package, destination, sources):
    return subprocess.run(['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', str(PREPARE),
                           '-Package', str(package), '-OutputDirectory', str(destination),
                           '-SourceDirectory', str(sources)], capture_output=True, timeout=20)


def fixture_package(path, name='Folimeld.Dev', publisher='CN=Takuma Yamada', architecture='x64'):
    with ZipFile(path, 'w') as archive:
        archive.writestr('AppxManifest.xml', f'<Package><Identity Name="{name}" Publisher="{publisher}" '
                         f'ProcessorArchitecture="{architecture}" Version="0.3.3.0" /></Package>')
        archive.writestr('Folimeld.exe', b'placeholder')


@pytest.mark.parametrize('identity', [dict(name='Production.App'), dict(publisher='CN=Different'), dict(architecture='arm64')])
def test_prepare_refuses_other_identities_before_creating_output(tmp_path, identity):
    package = tmp_path / 'input.msix'
    fixture_package(package, **identity)
    destination = tmp_path / 'bundle'
    result = run_prepare(package, destination, tmp_path)
    assert result.returncode != 0
    assert b'Only the Folimeld.Dev x64' in result.stderr
    assert not destination.exists()


def test_prepare_preserves_existing_bundle(tmp_path):
    package = tmp_path / 'input.msix'
    fixture_package(package)
    destination = tmp_path / 'bundle'
    destination.mkdir()
    original = destination / 'original.txt'
    original.write_text('keep')
    result = run_prepare(package, destination, tmp_path)
    assert result.returncode != 0 and b'existing bundles are preserved' in result.stderr
    assert original.read_text() == 'keep'
    assert list(destination.iterdir()) == [original]


def test_prepare_requires_matching_source_record_before_signing(tmp_path):
    package = tmp_path / 'input.msix'
    fixture_package(package)
    destination = tmp_path / 'bundle'
    assert run_prepare(package, destination, tmp_path).returncode != 0
    assert not destination.exists()


@pytest.mark.parametrize('name', ['prepare_msix_test.ps1', 'test_msix_on_vm.ps1'])
def test_powershell_scripts_parse(name):
    script = str(ROOT / 'tools' / name).replace("'", "''")
    command = "$tokens=$null; $errors=$null; [void][System.Management.Automation.Language.Parser]::ParseFile('" + script + "',[ref]$tokens,[ref]$errors); if ($errors.Count) { exit 1 }"
    result = subprocess.run(['powershell', '-NoProfile', '-Command', command], capture_output=True, timeout=20)
    assert result.returncode == 0, result.stderr
