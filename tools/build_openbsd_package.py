"""Stage captured sources and a native wheel, then build two OpenBSD ports."""

import argparse
import ast
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys

from tools.build_freebsd_package import extract, sha256


DEPENDENCY_SOURCES = {
    'pymupdf-1.28.2.tar.gz': '5e0be7908a715aa20333caddd73f1d6f01e4cd0c26e869fa2dd0b7f344da2249',
    'mupdf-1.28.2-source.tar.gz': '44075a84e329db55b9bef5f342a70fd26d69e48ad1d33cb89d9664581c641156',
}
WHEEL_SHA256 = '25932378ff47c85f5ef308120ff839472a261c3579bf77b3c370423f674c40b1'


def run(*args, **kwargs):
    environment = dict(os.environ, PORTS_TREE_OWNER='root', FAKE_TREE_OWNER='root')
    return subprocess.run(args, check=True, env=environment, **kwargs)


def make_port(directory, stage, package, dependencies, wantlib='', shared_libs=''):
    """Use ports for fake installation, shared-library checks and package metadata."""
    directory.mkdir(parents=True, exist_ok=True)
    pkg = directory / 'pkg'
    pkg.mkdir(exist_ok=True)
    (pkg / 'DESCR').write_text('Folimeld visual PDF editor and its private MuPDF runtime.\n')
    entries = []
    for path in sorted(stage.rglob('*')):
        name = path.relative_to(stage).as_posix()
        if path.is_dir():
            if name.startswith('share/folimeld'):
                entries.append(name + '/')
        elif '.so.' in path.name:
            library = path.name.split('.so.')[0].removeprefix('lib')
            entries.append('@lib ' + name.split('.so.')[0] + '.so.${LIB' + library + '_VERSION}')
        elif path.suffix == '.so':
            entries.append('@so ' + name)
        elif path.suffix == '.a':
            entries.append('@static-lib ' + name)
        else:
            entries.append(name)
    (pkg / 'PLIST').write_text('\n'.join(entries) + '\n')
    (directory / 'Makefile').write_text(
        'COMMENT = visual PDF editor runtime\n'
        f'PKGNAME = {package}\n'
        'CATEGORIES = print\n'
        'HOMEPAGE = https://github.com/tyamada/Folimeld\n'
        '# AGPL-3.0-only; matching sources and notices accompany the release.\n'
        'PERMIT_PACKAGE = Yes\n'
        'ONLY_FOR_ARCHS = amd64\n'
        'DISTFILES =\nNO_BUILD = Yes\nNO_TEST = Yes\n'
        f'RUN_DEPENDS = {dependencies}\n'
        f'WANTLIB = {wantlib}\n'
        f'SHARED_LIBS = {shared_libs}\n'
        f'PAYLOAD = {stage}\n'
        'do-install:\n\t${INSTALL_DATA_DIR} ${PREFIX}\n'
        '\tcp -Rp ${PAYLOAD}/. ${PREFIX}/\n'
        '.include <bsd.port.mk>\n')


def build(source_zip, wheel, dependency_sources, output, work, wheel_sha256=WHEEL_SHA256):
    if (platform.system(), platform.release(), platform.machine()) != ('OpenBSD', '8.0', 'amd64'):
        raise RuntimeError('Build on OpenBSD 8.0 amd64')
    if sys.version_info[:2] != (3, 14):
        raise RuntimeError('Python 3.14 is required')
    if sha256(wheel) != wheel_sha256:
        raise ValueError('Wheel differs from the verified LLVM 22 build')
    for name, expected in DEPENDENCY_SOURCES.items():
        if sha256(dependency_sources / name) != expected:
            raise ValueError(f'Dependency source mismatch: {name}')
    if work.exists():
        raise ValueError('Use a new work directory for each build')
    work.mkdir(parents=True)
    output.mkdir(parents=True, exist_ok=True)
    source = work / 'source'
    extract(source_zip, source)
    manifest = json.loads((source / 'SOURCE-MANIFEST.json').read_text())
    for name, expected in manifest['files'].items():
        path = source / name
        if not path.resolve().is_relative_to(source.resolve()) or sha256(path) != expected:
            raise ValueError(f'Source manifest mismatch: {name}')
    tree = ast.parse((source / 'folimeld/__init__.py').read_text())
    version = next(ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign)
                   and any(isinstance(t, ast.Name) and t.id == '__version__' for t in n.targets))
    app_stage = work / 'app-stage'
    app = app_stage / 'share/folimeld'
    app.mkdir(parents=True)
    for name in ('folimeld', 'assets', 'locales', 'licenses'):
        shutil.copytree(source / name, app / name,
                        ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    for name in ('main.py', 'LICENSE'):
        shutil.copy2(source / name, app / name)
    native_stage = work / 'native-stage'
    vendor = native_stage / 'share/folimeld/vendor'
    extract(wheel, vendor)
    for target, origin in (
        ('share/applications/folimeld.desktop', 'packaging/linux/folimeld.desktop'),
        ('share/icons/hicolor/128x128/apps/folimeld.png', 'assets/Folimeld.iconset/icon_128x128.png'),
    ):
        path = app_stage / target
        path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source / origin, path)
    binary = app_stage / 'bin/folimeld'
    binary.parent.mkdir()
    binary.write_text('#!/bin/sh\nexport PYTHONNOUSERSITE=1\n'
                      'export PYTHONPATH=/usr/local/share/folimeld/vendor:/usr/local/share/folimeld\n'
                      'exec /usr/local/bin/python3.14 /usr/local/share/folimeld/main.py "$@"\n')
    binary.chmod(0o755)
    record = {'source_archive': source_zip.name, 'source_sha256': sha256(source_zip),
              'git_commit': manifest['git_commit'], 'working_tree_changed': manifest['working_tree_changed'],
              'wheel': wheel.name, 'wheel_sha256': sha256(wheel),
              'dependency_sources': DEPENDENCY_SOURCES, 'platform': platform.platform(),
              'python': sys.version, 'ports': {}, 'packages': {}}
    (app / 'licenses/Build-source.txt').write_text(json.dumps(record, indent=2) + '\n')
    native_port = Path('/usr/ports/print/folimeld-mupdf')
    app_port = Path('/usr/ports/print/folimeld')
    if native_port.exists() or app_port.exists():
        raise ValueError('Local ports already exist; inspect before rebuilding')
    make_port(native_port, native_stage, 'folimeld-mupdf-1.28.2',
              'python->=3.14,<3.15:lang/python/3 gettext-runtime-*:devel/gettext,-runtime',
              'c c++ c++abi crypto iconv intl m pthread util', 'mupdf 28.2 mupdfcpp 28.2')
    make_port(app_port, app_stage, f'folimeld-{version}',
              'folimeld-mupdf->=1.28.2,<1.28.3:print/folimeld-mupdf '
              'python->=3.14,<3.15:lang/python/3 pyside6-*:x11/qt6/pyside6/pyside '
              'py3-Pillow->=11:graphics/py-Pillow '
              'py3-cryptography->=46,<51:security/py-cryptography '
              'py3-psutil-*:sysutils/py-psutil noto-cjk-*:fonts/noto/cjk')
    for port in (native_port, app_port):
        run('make', 'fake', cwd=port)
        run('make', 'package', cwd=port)
        name = 'folimeld-mupdf-1.28.2' if port == native_port else f'folimeld-{version}'
        artifact = Path('/usr/ports/packages/amd64/all') / (name + '.tgz')
        shutil.copy2(artifact, output / artifact.name)
        record['packages'][artifact.name] = sha256(artifact)
        record['ports'][port.name] = (port / 'Makefile').read_text()
    record['installed_packages'] = subprocess.check_output(['pkg_info', '-a'], text=True)
    record['payload_files'] = {str(p.relative_to(stage)): sha256(p)
                               for stage in (app_stage, native_stage)
                               for p in stage.rglob('*') if p.is_file()}
    (output / 'build-record.json').write_text(json.dumps(record, indent=2) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('source', 'wheel', 'dependency-sources', 'output', 'work'):
        parser.add_argument('--' + name, type=Path, required=True)
    parser.add_argument('--wheel-sha256', default=WHEEL_SHA256,
                        help='Expected hash; supply the recorded hash when rebuilding the wheel')
    args = parser.parse_args()
    build(args.source.resolve(), args.wheel.resolve(), args.dependency_sources.resolve(),
          args.output.resolve(), args.work.resolve(), args.wheel_sha256)


if __name__ == '__main__':
    main()
