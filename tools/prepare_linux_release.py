"""Verify existing Linux release assets and write an offline migration manifest.

No build, tag, upload, publication, or deletion is performed. Windows and macOS
binaries are never selected. Run from a checkout containing releases/ubuntu.
"""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
from zipfile import BadZipFile, ZipFile


VERSION = re.compile(r"[0-9]+\.[0-9]+\.[0-9]+")
SOURCE_NAME = re.compile(r"Folimeld-source-([0-9a-f]{64})\.zip")


def checksum(path):
    result = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            result.update(chunk)
    return result.hexdigest()


def prepare(root, version):
    if not VERSION.fullmatch(version):
        raise ValueError('Use a numeric major.minor.patch version')
    root = Path(root).resolve()
    base = root / 'releases/ubuntu'
    sums = base / f'folimeld_{version}_SHA256SUMS.txt'
    expected = {f'folimeld_{version}_{arch}.{kind}' for arch in ('amd64', 'arm64') for kind in ('deb', 'snap')}
    hashes = {}
    for line in sums.read_text().splitlines():
        digest, name = line.split(maxsplit=1)
        if name not in expected or name in hashes or not re.fullmatch('[0-9a-f]{64}', digest):
            raise ValueError('Unexpected/duplicate package in checksum list')
        hashes[name] = digest
    if set(hashes) != expected:
        raise ValueError('Expected exactly four Linux packages')
    assets = {}
    warnings = set()
    commits = set()

    def add(path, role, expected_digest=None):
        if path.is_symlink():
            raise ValueError('Symlink release assets are not supported')
        path = path.resolve()
        if not path.is_relative_to(base.resolve()) or not path.is_file():
            raise ValueError('Unsafe/missing release asset')
        digest = checksum(path)
        if expected_digest is not None and digest != expected_digest:
            raise ValueError(f'Checksum mismatch: {path.name}')
        if path.name in assets:
            if assets[path.name]['sha256'] != digest:
                raise ValueError('Conflicting release asset name')
            return
        assets[path.name] = dict(path=path.relative_to(root).as_posix(), name=path.name,
                                 bytes=path.stat().st_size, sha256=digest, role=role)

    add(sums, 'package-checksums')
    for name, digest in sorted(hashes.items()):
        add(base / name, 'linux-package', digest)
        arch = name.rsplit('_', 1)[1].split('.')[0]
        folder = base / 'source' / f'{version}-{arch}'
        record = folder / f'{name}-{digest}.json'
        data = json.loads(record.read_text())
        if data['artifact'] != name or data['artifact_sha256'] != digest:
            raise ValueError('Package/source record mismatch')
        source_name = data['source_archive']
        match = SOURCE_NAME.fullmatch(source_name)
        if match is None or data['source_sha256'] != match[1]:
            raise ValueError('Unsafe/inconsistent source archive name')
        source = folder / source_name
        add(record, 'artifact-source-record')
        add(source, 'folimeld-source', data['source_sha256'])
        sidecar = source.with_suffix('.json')
        source_record = json.loads(sidecar.read_text())
        if source_record['source_archive'] != source_name or source_record['source_sha256'] != data['source_sha256']:
            raise ValueError('Source sidecar mismatch')
        add(sidecar, 'build-source-record')
        with ZipFile(source) as archive:
            manifest = json.loads(archive.read('SOURCE-MANIFEST.json'))
            if manifest['files'] != source_record['files']:
                raise ValueError('Embedded source manifest mismatch')
            for member, member_digest in manifest['files'].items():
                relative = PurePosixPath(member)
                if (relative.is_absolute() or '..' in relative.parts or '\\' in member
                        or relative.suffix.lower() in {'.exe', '.dll', '.pyd', '.msix', '.msixbundle',
                                                       '.appx', '.dmg', '.pkg', '.dylib', '.pfx', '.p12', '.key'}
                        or any(part.lower().endswith('.app') for part in relative.parts)):
                    raise ValueError('Unsafe/private binary in source archive')
                if hashlib.sha256(archive.read(member)).hexdigest() != member_digest:
                    raise ValueError('Source member checksum mismatch')
        if data.get('git_commit'):
            commits.add(data['git_commit'])
        if source_record.get('working_tree_changed'):
            warnings.add('Build sources contain uncommitted changes; the attached source ZIP, not a tag archive, identifies the build inputs.')
        if str(data.get('dependency_sources', '')).startswith('NOT INCLUDED'):
            warnings.add('The existing records mark matching dependency sources as not included; migration does not resolve this recorded release-readiness gap.')
    return dict(version=version, proposed_tag=f'linux-v{version}',
                policy='Public Linux packages only; Windows/macOS binaries remain private.',
                publication_performed=False, recorded_build_commits=sorted(commits),
                total_bytes=sum(a['bytes'] for a in assets.values()),
                assets=sorted(assets.values(), key=lambda a: a['name']), warnings=sorted(warnings))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--version', default='0.3.3')
    parser.add_argument('--output', type=Path, default=Path('build/linux-release-plan.json'))
    args = parser.parse_args()
    try:
        plan = prepare(Path(__file__).resolve().parents[1], args.version)
    except (ValueError, KeyError, OSError, BadZipFile) as error:
        parser.exit(1, f'Release asset verification failed: {error}\n')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Verified {len(plan["assets"])} Linux/source assets; manifest: {args.output}')
    for warning in plan['warnings']:
        print(f'Note: {warning}')


if __name__ == '__main__':
    main()
