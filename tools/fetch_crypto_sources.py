"""Collect native crypto sources/notices without executing downloaded code.

Requires the exact cryptography/CFFI sdists and JSON records produced by
fetch_dependency_sources.py. Cargo.lock includes build-only dependencies;
this inventory is a conservative source set, not a compiled-code SBOM.
"""

import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
from importlib.metadata import distribution
import json
from pathlib import Path
import platform
import re
import tarfile
import tomllib
from urllib.request import urlopen


def checksum(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def download(url, destination, expected):
    if not re.fullmatch(r'[0-9a-f]{64}', expected):
        raise ValueError('Invalid SHA-256')
    if destination.exists() and checksum(destination) == expected:
        return
    temporary = destination.with_suffix(destination.suffix + '.part')
    try:
        with urlopen(url, timeout=60) as response, temporary.open('wb') as stream:
            while block := response.read(1024 * 1024):
                stream.write(block)
        if checksum(temporary) != expected:
            raise ValueError(f'Checksum mismatch: {destination.name}')
        temporary.replace(destination)
    finally:
        temporary.unlink(missing_ok=True)


def verified_sdist(directory, name, version):
    record = json.loads((directory / f'{name}=={version}.json').read_text(encoding='utf-8'))
    if record['package'] != f'{name}=={version}' or len(record.get('files', [])) != 1:
        raise ValueError('Expected one matching source distribution')
    entry = record['files'][0]
    if Path(entry['filename']).name != entry['filename'] or '\\' in entry['filename']:
        raise ValueError('Unsafe source filename')
    path = directory / entry['filename']
    if checksum(path) != entry['sha256']:
        raise ValueError(f'Source checksum mismatch: {name}')
    return path


def legal_texts(path):
    """Read legal documents directly; never extract archive paths to disk."""
    sections = []
    with tarfile.open(path) as archive:
        for member in sorted(archive.getmembers(), key=lambda m: m.name):
            basename = member.name.rsplit('/', 1)[-1].lower()
            if member.isfile() and basename.startswith(('license', 'copying', 'notice', 'copyright')):
                data = archive.extractfile(member).read().decode('utf-8', errors='replace')
                sections.append(f'--- {member.name} ---\n{data}')
    if not sections:
        raise ValueError(f'No license documents found: {path.name}')
    return '\n\n'.join(sections)


def collect(directory, notices, crypto_version, cffi_version, openssl_version):
    for version in (crypto_version, cffi_version, openssl_version):
        if not re.fullmatch(r'[0-9]+\.[0-9]+\.[0-9]+', version):
            raise ValueError('Expected a stable three-part version')
    from cryptography.hazmat.backends.openssl.backend import backend

    if backend.openssl_version_text().split()[1] != openssl_version:
        raise ValueError('OpenSSL version does not match the installed cryptography backend')
    binaries = {}
    for name, version in [('cryptography', crypto_version), ('cffi', cffi_version)]:
        dist = distribution(name)
        if dist.version != version:
            raise ValueError(f'Installed {name} version does not match requested source')
        for file in dist.files or []:
            if str(file).endswith(('.pyd', '.so', '.dylib')):
                binaries[str(file)] = checksum(dist.locate_file(file))
    crypto = verified_sdist(directory, 'cryptography', crypto_version)
    cffi = verified_sdist(directory, 'cffi', cffi_version)
    with tarfile.open(crypto) as archive:
        lock_bytes = archive.extractfile(f'cryptography-{crypto_version}/Cargo.lock').read()
    lock = tomllib.loads(lock_bytes.decode('utf-8'))
    crates = []
    for package in lock['package']:
        if 'source' not in package:
            continue
        if package['source'] != 'registry+https://github.com/rust-lang/crates.io-index':
            raise ValueError('Unexpected Cargo source; review manually')
        name, version = package['name'], package['version']
        if not re.fullmatch(r'[a-zA-Z0-9_-]+', name) or not re.fullmatch(r'[0-9A-Za-z.+-]+', version):
            raise ValueError('Unsafe crate name/version')
        crates.append({'name': name, 'version': version, 'sha256': package['checksum'],
                       'filename': f'{name}-{version}.crate',
                       'url': f'https://static.crates.io/crates/{name}/{name}-{version}.crate'})
    crate_dir = directory / 'cryptography-rust'
    crate_dir.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(lambda p: download(p['url'], crate_dir / p['filename'], p['sha256']), crates))
    filename = f'openssl-{openssl_version}.tar.gz'
    url = f'https://github.com/openssl/openssl/releases/download/openssl-{openssl_version}/{filename}'
    with urlopen(url + '.sha256', timeout=60) as response:
        upstream = response.read().decode('ascii').strip()
    expected = upstream.split()[0].lower()
    openssl = directory / filename
    download(url, openssl, expected)
    notices.mkdir(parents=True, exist_ok=True)
    rust_text = ['cryptography Cargo.lock dependency notices (includes build dependencies).']
    for p in crates:
        rust_text.append(f"{p['name']} {p['version']}\n{p['url']}\nSHA256: {p['sha256']}\n\n"
                         + legal_texts(crate_dir / p['filename']))
    ffi_text = [f'CFFI {cffi_version}: notices from bundled x86/x64 libffi source headers.']
    with tarfile.open(cffi) as archive:
        for member in sorted(archive.getmembers(), key=lambda m: m.name):
            if member.isfile() and '/src/c/libffi_x86_x64/' in member.name and member.name.endswith(('.c', '.h')):
                text = archive.extractfile(member).read().decode('utf-8')
                header = re.match(r'\s*(/\*.*?\*/)', text, re.DOTALL)
                if header and 'copyright' in header[1].lower():
                    ffi_text.append(f'--- {member.name} ---\n{header[1]}')
    if len(ffi_text) == 1:
        raise ValueError('No bundled libffi copyright headers found')
    texts = {'Cryptography-Rust.txt': '\n\n'.join(rust_text),
             'CFFI-libffi-x64.txt': '\n\n'.join(ffi_text),
             'OpenSSL.txt': f'OpenSSL {openssl_version}\n{url}\nSHA256: {expected}\n\n' + legal_texts(openssl)}
    for name, text in texts.items():
        (notices / name).write_text(text + '\n', encoding='utf-8')
    record = {'cryptography_version': crypto_version, 'cffi_version': cffi_version,
              'openssl_version': openssl_version, 'cargo_lock_sha256': hashlib.sha256(lock_bytes).hexdigest(),
              'platform': platform.platform(), 'machine': platform.machine(),
              'installed_native_binary_sha256': binaries,
              'source_archive_sha256': {crypto.name: checksum(crypto), cffi.name: checksum(cffi)},
              'crates': crates, 'openssl': {'url': url, 'sha256_url': url + '.sha256', 'sha256': expected},
              'notice_sha256': {name: checksum(notices / name) for name in texts},
              'scope': 'Cargo.lock superset; CFFI x86/x64 headers; upstream OpenSSL legal files. '
                       'Not proof of wheel build provenance, complete native notices, or all-platform compliance.'}
    (notices / 'crypto-native-sources.json').write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
    print(f'Verified {len(crates)} crates and OpenSSL {openssl_version}; notices: {notices}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sources', type=Path, default=Path('dist/source/dependencies'))
    parser.add_argument('--notices', type=Path, default=Path('build/legal/crypto-native'))
    parser.add_argument('--cryptography-version', required=True)
    parser.add_argument('--cffi-version', required=True)
    parser.add_argument('--openssl-version', required=True)
    args = parser.parse_args()
    collect(args.sources, args.notices, args.cryptography_version, args.cffi_version, args.openssl_version)


if __name__ == '__main__':
    main()
