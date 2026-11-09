"""Build a native pkg from a captured source ZIP and a FreeBSD PyMuPDF wheel."""

import argparse
import ast
import hashlib
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile
from zipfile import ZipFile


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def extract(archive, destination):
    with ZipFile(archive) as bundle:
        for item in bundle.infolist():
            if not (destination / item.filename).resolve().is_relative_to(destination.resolve()):
                raise ValueError(f'Unsafe archive member: {item.filename}')
            if item.external_attr >> 16 & 0o170000 == 0o120000:
                raise ValueError(f'Symlink archive member: {item.filename}')
        bundle.extractall(destination)


def build(source_zip, wheel, output):
    if platform.system() != 'FreeBSD' or platform.machine() != 'amd64' or sys.version_info[:2] != (3, 12):
        raise RuntimeError('Build on FreeBSD amd64 with Python 3.12')
    if 'freebsd' not in wheel.name or '1.28.2-' not in wheel.name:
        raise ValueError('A FreeBSD PyMuPDF 1.28.2 wheel is required')
    output.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='folimeld-pkg-') as temporary:
        work = Path(temporary)
        source = work / 'source'
        extract(source_zip, source)
        record = json.loads((source / 'SOURCE-MANIFEST.json').read_text())
        for name, expected in record['files'].items():
            path = source / name
            if not path.resolve().is_relative_to(source.resolve()) or sha256(path) != expected:
                raise ValueError(f'Source manifest mismatch: {name}')
        stage = work / 'stage'
        app = stage / 'usr/local/share/folimeld'
        app.mkdir(parents=True)
        for name in ('folimeld', 'assets', 'locales', 'licenses'):
            shutil.copytree(source / name, app / name)
        for name in ('main.py', 'LICENSE'):
            shutil.copy2(source / name, app / name)
        extract(wheel, app / 'vendor')
        tree = ast.parse((source / 'folimeld/__init__.py').read_text())
        version = next(ast.literal_eval(node.value) for node in tree.body
                       if isinstance(node, ast.Assign)
                       and any(isinstance(t, ast.Name) and t.id == '__version__' for t in node.targets)) + '_1'
        dependencies = {}
        for name in ('python312', 'py312-pyside6', 'py312-pillow', 'py312-cryptography',
                     'py312-psutil', 'noto-sans-jp'):
            values = subprocess.check_output(['pkg', 'query', '%n|%o|%v', name], text=True).strip().split('|')
            if len(values) != 3:
                raise RuntimeError(f'Missing or ambiguous dependency: {name}')
            dependencies[values[0]] = {'origin': values[1], 'version': values[2]}
        binary = stage / 'usr/local/bin/folimeld'
        binary.parent.mkdir(parents=True)
        binary.write_text('#!/bin/sh\nexport PYTHONPATH="/usr/local/share/folimeld/vendor:/usr/local/share/folimeld"\nexec /usr/local/bin/python3.12 /usr/local/share/folimeld/main.py "$@"\n')
        binary.chmod(0o755)
        desktop = stage / 'usr/local/share/applications/folimeld.desktop'
        desktop.parent.mkdir(parents=True)
        shutil.copy2(source / 'packaging/linux/folimeld.desktop', desktop)
        icon = stage / 'usr/local/share/icons/hicolor/128x128/apps/folimeld.png'
        icon.parent.mkdir(parents=True)
        shutil.copy2(source / 'assets/Folimeld.iconset/icon_128x128.png', icon)
        build_record = {'source_archive': source_zip.name, 'source_sha256': sha256(source_zip),
                        'wheel': wheel.name, 'wheel_sha256': sha256(wheel),
                        'platform': platform.platform(), 'python': sys.version, 'dependencies': dependencies}
        (app / 'licenses/Build-source.txt').write_text(json.dumps(build_record, indent=2) + '\n')
        files = {'/' + p.relative_to(stage).as_posix():
                 {'sum': sha256(p), 'uname': 'root', 'gname': 'wheel',
                  'perm': '0755' if p == binary else '0644'}
                 for p in stage.rglob('*') if p.is_file()}
        manifest = {'name': 'folimeld', 'version': version, 'origin': 'deskutils/folimeld',
                    'comment': 'Visual PDF page editor', 'desc': 'Local PDF editing with Qt and MuPDF.',
                    'www': 'https://github.com/tyamada/Folimeld', 'maintainer': 'takuma.yamada22@gmail.com',
                    'prefix': '/usr/local', 'licenselogic': 'single', 'licenses': ['AGPLv3'],
                    'arch': subprocess.check_output(['pkg', 'config', 'ABI'], text=True).strip(),
                    'deps': dependencies, 'flatsize': sum(p.stat().st_size for p in stage.rglob('*') if p.is_file()),
                    'files': files}
        manifest_path = work / 'manifest.json'
        manifest_path.write_text(json.dumps(manifest))
        subprocess.run(['pkg', 'create', '-r', str(stage), '-M', str(manifest_path), '-o', str(output)], check=True)
        package = output / f'folimeld-{version}.pkg'
        build_record.update(package=package.name, package_sha256=sha256(package))
        (output / 'build-record.json').write_text(json.dumps(build_record, indent=2) + '\n')
        print(package)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--wheel', type=Path, required=True)
    parser.add_argument('--output', type=Path, default=Path('dist/freebsd'))
    args = parser.parse_args()
    build(args.source.resolve(), args.wheel.resolve(), args.output.resolve())


if __name__ == '__main__':
    main()
