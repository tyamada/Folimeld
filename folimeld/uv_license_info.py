"""License view for the explicitly activated Windows source/uv profile."""
import hashlib
from importlib.metadata import PackageNotFoundError, version
import json
from pathlib import Path
import sys


def uv_license_documents(root: Path) -> list[tuple[str, str]]:
    """Use the pinned uv inventory; never substitute a frozen build's notices."""
    import platform
    is_arm64 = platform.machine().lower() in {'arm64', 'aarch64'}
    directory = root / 'documentation' / 'windows-arm64-uv-licenses' if is_arm64 and (root / 'documentation' / 'windows-arm64-uv-licenses').exists() else root / 'documentation' / 'windows-uv-licenses'
    profile_path = root / 'windows-arm64-uv-runtime.json' if is_arm64 and (root / 'windows-arm64-uv-runtime.json').exists() else root / 'windows-uv-runtime.json'
    ledger_text = (directory / 'sources.json').read_text(encoding='utf-8')
    ledger = json.loads(ledger_text)
    profile = json.loads(profile_path.read_text(encoding='utf-8'))
    packages = ledger['packages']
    pins = {item['name']: item['version'] for item in packages}
    if ledger['schema_version'] != 1 or len(pins) != len(packages) or pins != profile['dependencies']:
        raise ValueError('The uv license inventory differs from the runtime profile.')
    if ledger['runtime_lock_sha256'] != profile['lock_sha256']:
        raise ValueError('The uv license inventory differs from the runtime lock.')
    for name in ('python', 'uv'):
        for key in ('version', 'url', 'sha256'):
            if ledger[name][key] != profile[name][key]:
                raise ValueError(f'The uv license inventory differs for {name}.')
    if ledger['python']['build'] != profile['python']['build']:
        raise ValueError('The uv license inventory differs for the Python build.')
    notice_bytes = (directory / 'notices.txt').read_bytes()
    # Source checkouts may normalize CRLF; hash the documented UTF-8/LF form.
    notice = notice_bytes.decode('utf-8').replace('\r\n', '\n')
    if hashlib.sha256(notice.encode('utf-8')).hexdigest() != ledger['notice_sha256']:
        raise ValueError('The uv license notice hash does not match its inventory.')
    observed = [f'Python (current): {sys.version}',
                'Pinned environment; runtime dependencies only. PyInstaller is not used.',
                'Version matches are not evidence of byte-identical binaries or source builds.']
    for name, expected in pins.items():
        try:
            actual = version(name)
        except PackageNotFoundError:
            actual = 'not installed'
        status = 'matches pin' if actual == expected else 'DIFFERS FROM PIN'
        observed.append(f'{name}: installed {actual}; pinned {expected}; {status}')
    observed.append(f"uv {profile['uv']['version']}: installer-verified archive; "
                    'not re-executed by this license view.')
    return [('Folimeld', (root / 'LICENSE').read_text(encoding='utf-8')),
            ('Windows uv notices', notice),
            ('Windows uv installed packages', '\n'.join(observed)),
            ('Windows uv sources', ledger_text)]
