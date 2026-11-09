import hashlib
import json
from zipfile import ZipFile

import pytest

from tools.prepare_linux_release import prepare


@pytest.fixture
def linux_release(tmp_path, request):
    member = getattr(request, "param", "main.py")
    base = tmp_path / 'releases/ubuntu'
    base.mkdir(parents=True)
    sums = []
    for arch in ('amd64', 'arm64'):
        folder = base / 'source' / f'0.3.3-{arch}'
        folder.mkdir(parents=True)
        for kind in ('deb', 'snap'):
            name = f'folimeld_0.3.3_{arch}.{kind}'
            data = name.encode()
            digest = hashlib.sha256(data).hexdigest()
            (base / name).write_bytes(data)
            sums.append(f'{digest}  {name}')
            contents = {member: hashlib.sha256(data).hexdigest()}
            draft = folder / 'source.zip'
            with ZipFile(draft, 'w') as archive:
                archive.writestr(member, data)
                archive.writestr('SOURCE-MANIFEST.json', json.dumps({'files': contents}))
            source_hash = hashlib.sha256(draft.read_bytes()).hexdigest()
            source_name = f'Folimeld-source-{source_hash}.zip'
            draft.rename(folder / source_name)
            record = dict(artifact=name, artifact_sha256=digest,
                          source_archive=source_name, source_sha256=source_hash,
                          git_commit='base-commit', dependency_sources='NOT INCLUDED: review sources')
            (folder / f'{name}-{digest}.json').write_text(json.dumps(record))
            source = dict(source_archive=source_name, source_sha256=source_hash,
                          files=contents, working_tree_changed=True)
            (folder / source_name).with_suffix('.json').write_text(json.dumps(source))
    (base / 'folimeld_0.3.3_SHA256SUMS.txt').write_text('\n'.join(sums) + '\n')
    return tmp_path


def test_only_verified_linux_and_corresponding_sources_are_selected(linux_release):
    (linux_release / 'releases/ubuntu/private.exe').write_bytes(b'private')
    (linux_release / 'releases/ubuntu/private.dmg').write_bytes(b'private')
    result = prepare(linux_release, '0.3.3')
    assert len(result['assets']) == 17
    assert len([a for a in result['assets'] if a['role'] == 'linux-package']) == 4
    assert all('private' not in a['name'] for a in result['assets'])
    assert result['publication_performed'] is False
    assert len(result['warnings']) == 2


def test_corrupted_package_is_rejected(linux_release):
    (linux_release / 'releases/ubuntu/folimeld_0.3.3_amd64.deb').write_bytes(b'changed')
    with pytest.raises(ValueError, match='Checksum mismatch'):
        prepare(linux_release, '0.3.3')


def test_private_binary_in_checksum_list_is_rejected(linux_release):
    sums = linux_release / 'releases/ubuntu/folimeld_0.3.3_SHA256SUMS.txt'
    sums.write_text(sums.read_text() + '0' * 64 + '  Folimeld.exe\n')
    with pytest.raises(ValueError, match='Unexpected'):
        prepare(linux_release, '0.3.3')


def test_wrong_source_archive_association_is_rejected(linux_release):
    record = next((linux_release / 'releases/ubuntu/source').rglob('folimeld_*.json'))
    data = json.loads(record.read_text())
    data['source_archive'] = '../private.zip'
    record.write_text(json.dumps(data))
    with pytest.raises(ValueError, match='Unsafe'):
        prepare(linux_release, '0.3.3')


def test_source_manifest_mismatch_is_rejected(linux_release):
    sidecar = next((linux_release / 'releases/ubuntu/source').rglob('Folimeld-source-*.json'))
    data = json.loads(sidecar.read_text())
    data['files'] = {}
    sidecar.write_text(json.dumps(data))
    with pytest.raises(ValueError, match='manifest mismatch'):
        prepare(linux_release, '0.3.3')


@pytest.mark.parametrize('version', ['../private', '0.3.3/../../', 'latest'])
def test_unsafe_version_is_rejected(linux_release, version):
    with pytest.raises(ValueError, match='numeric'):
        prepare(linux_release, version)


@pytest.mark.parametrize('linux_release', ['private.exe'], indirect=True)
def test_private_binary_inside_source_archive_is_rejected(linux_release):
    with pytest.raises(ValueError, match='private binary'):
        prepare(linux_release, '0.3.3')
