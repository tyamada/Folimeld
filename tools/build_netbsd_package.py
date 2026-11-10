"""Create a NetBSD pkg_install package from captured sources and native libraries."""

import argparse
import ast
import hashlib
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tarfile
import tempfile

from tools.build_freebsd_package import extract, sha256


DEPENDENCY_SOURCES = {
    'pyside-setup-everywhere-src-6.11.2.tar.xz': 'cba47efbaad1bedd529725cbc14e21f156c7a19366f07b3edfbb076ffd7afdf8',
    'pymupdf-1.28.2.tar.gz': '5e0be7908a715aa20333caddd73f1d6f01e4cd0c26e869fa2dd0b7f344da2249',
    'mupdf-1.28.2-source.tar.gz': '44075a84e329db55b9bef5f342a70fd26d69e48ad1d33cb89d9664581c641156',
}


def build(source_zip, native_prefix, dependency_sources, output):
    if platform.system() != 'NetBSD' or platform.machine() not in ('amd64', 'evbarm') or sys.version_info[:2] != (3, 12):
        raise RuntimeError('Build on NetBSD amd64 or aarch64 with Python 3.12')
    output.mkdir(parents=True, exist_ok=True)
    arch = subprocess.check_output(['/sbin/sysctl', '-n', 'hw.machine_arch'], text=True).strip()
    if arch not in ('x86_64', 'aarch64'):
        raise RuntimeError(f'Unsupported NetBSD package ABI: {arch}')
    for name, expected in DEPENDENCY_SOURCES.items():
        if sha256(dependency_sources / name) != expected:
            raise ValueError(f'Dependency source hash mismatch: {name}')
    with tempfile.TemporaryDirectory(prefix='folimeld-netbsd-') as temporary:
        work = Path(temporary)
        source = work / 'source'
        extract(source_zip, source)
        manifest = json.loads((source / 'SOURCE-MANIFEST.json').read_text())
        for name, expected in manifest['files'].items():
            path = source / name
            if not path.resolve().is_relative_to(source.resolve()) or sha256(path) != expected:
                raise ValueError(f'Source manifest mismatch: {name}')
        stage = work / 'stage'
        app = stage / 'share/folimeld'
        app.mkdir(parents=True)
        for name in ('folimeld', 'assets', 'locales', 'licenses'):
            shutil.copytree(source / name, app / name)
        for name in ('main.py', 'LICENSE'):
            shutil.copy2(source / name, app / name)
        with tarfile.open(dependency_sources / 'pyside-setup-everywhere-src-6.11.2.tar.xz') as archive:
            for member in archive.getmembers():
                if member.isfile() and '/LICENSES/' in member.name:
                    path = app / 'licenses/PySide6' / Path(member.name).name
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_bytes(archive.extractfile(member).read())
        vendor = app / 'vendor'
        vendor.mkdir()
        site = native_prefix / 'lib/python3.12/site-packages'
        for name in ('PySide6', 'shiboken6', 'pymupdf', 'fitz', 'pymupdf-1.28.2.dist-info'):
            shutil.copytree(site / name, vendor / name,
                            ignore=shutil.ignore_patterns('__pycache__', '*.pyc'), symlinks=False)
        libraries = app / 'lib'
        libraries.mkdir()
        for pattern in ('libpyside6*.so*', 'libshiboken6*.so*'):
            for path in (native_prefix / 'lib').glob(pattern):
                shutil.copy2(path, libraries / path.name)
        tree = ast.parse((source / 'folimeld/__init__.py').read_text())
        version = next(ast.literal_eval(node.value) for node in tree.body
                       if isinstance(node, ast.Assign)
                       and any(isinstance(t, ast.Name) and t.id == '__version__' for t in node.targets))
        dependencies = []
        for name in ('python312', 'qt6-qtbase', 'qt6-qtsvg', 'qt6-qtimageformats',
                     'qt6-qttranslations', 'py312-Pillow', 'py312-cryptography',
                     'py312-psutil', 'noto-cjk-fonts', 'gettext-lib'):
            value = subprocess.check_output(['/usr/pkg/sbin/pkg_info', '-e', name + '-[0-9]*'], text=True).strip()
            if not value or '\n' in value:
                raise RuntimeError(f'Missing or ambiguous dependency: {name}')
            dependencies.append(value)
        binary = stage / 'bin/folimeld'
        binary.parent.mkdir()
        binary.write_text('#!/bin/sh\n'
                          'export PYTHONNOUSERSITE=1\n'
                          'export PYTHONPATH=/usr/pkg/share/folimeld/vendor:/usr/pkg/share/folimeld\n'
                          'export LD_LIBRARY_PATH=/usr/pkg/share/folimeld/lib:/usr/pkg/lib:/usr/X11R7/lib\n'
                          'exec /usr/pkg/bin/python3.12 /usr/pkg/share/folimeld/main.py "$@"\n')
        binary.chmod(0o755)
        for target, origin in (
            ('share/applications/folimeld.desktop', 'packaging/linux/folimeld.desktop'),
            ('share/icons/hicolor/128x128/apps/folimeld.png', 'assets/Folimeld.iconset/icon_128x128.png'),
        ):
            path = stage / target
            path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source / origin, path)
        files = sorted(p.relative_to(stage).as_posix() for p in stage.rglob('*') if p.is_file())
        packing = work / 'PLIST'
        packing.write_text('@name folimeld-' + version + '\n@cwd /usr/pkg\n' +
                           ''.join('@pkgdep ' + dep + '\n' for dep in dependencies) +
                           '\n'.join(files) + '\n')
        info = work / 'BUILD_INFO'
        info.write_text('OPSYS=NetBSD\nOS_VERSION=' + platform.release() +
                        f'\nMACHINE_ARCH={arch}\nPKGTOOLS_VERSION=' +
                        subprocess.check_output(['/usr/pkg/sbin/pkg_create', '-V'], text=True).strip() +
                        '\nLICENSE=gnu-agpl-v3\n')
        package = output / f'folimeld-{version}.tgz'
        subprocess.run(['/usr/pkg/sbin/pkg_create', '-p', str(stage), '-I', '/usr/pkg',
                        '-u', 'root', '-g', 'wheel', '-B', str(info), '-f', str(packing),
                        '-c', '-Visual PDF page editor', '-d', f'-Folimeld for NetBSD {arch}.',
                        str(package)], check=True)
        record = {'platform': platform.platform(), 'python': sys.version,
                  'source': source_zip.name, 'source_sha256': sha256(source_zip),
                  'dependency_sources': DEPENDENCY_SOURCES,
                  'dependencies': dependencies, 'files': len(files),
                  'package': package.name, 'package_sha256': sha256(package),
                  'native_files': {str(p.relative_to(app)): hashlib.sha256(p.read_bytes()).hexdigest()
                                   for directory in (vendor, libraries)
                                   for p in directory.rglob('*') if p.is_file()}}
        (output / 'build-record.json').write_text(json.dumps(record, indent=2) + '\n')
        print(package)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--native-prefix', type=Path, required=True)
    parser.add_argument('--dependency-sources', type=Path, required=True)
    parser.add_argument('--output', type=Path, default=Path('dist/netbsd'))
    args = parser.parse_args()
    build(args.source.resolve(), args.native_prefix.resolve(), args.dependency_sources.resolve(),
          args.output.resolve())


if __name__ == '__main__':
    main()
