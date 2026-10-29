"""Prepare and inspect MSIX packages without installing or submitting them."""
import argparse
import hashlib
from html import escape
import json
from pathlib import Path, PurePosixPath
import re
import struct
import xml.etree.ElementTree as ET
from zipfile import BadZipFile, ZipFile

from PIL import Image

from folimeld import __version__
from tools.write_version_info import windows_version


ROOT = Path(__file__).resolve().parent.parent
NS = {'p': 'http://schemas.microsoft.com/appx/manifest/foundation/windows10',
      'uap': 'http://schemas.microsoft.com/appx/manifest/uap/windows10',
      'rescap': 'http://schemas.microsoft.com/appx/manifest/foundation/windows10/restrictedcapabilities'}
CONFIG_KEYS = {'identity_name', 'publisher', 'publisher_display_name', 'package_version',
               'minimum_windows_version', 'maximum_tested_windows_version'}


def version_tuple(value):
    if not isinstance(value, str) or not re.fullmatch(r'(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)', value):
        raise ValueError('A version must contain four decimal components without leading zeros.')
    parts = tuple(map(int, value.split('.')))
    if any(part > 65535 for part in parts):
        raise ValueError('Version components must not exceed 65535.')
    return parts


def validate_config(config):
    for key in CONFIG_KEYS:
        value = config.get(key)
        if not isinstance(value, str) or not value.strip() or value != value.strip():
            raise ValueError(f'{key} must be a nonempty string without surrounding whitespace.')
    if config.get('architecture') not in ('x64', 'arm64'):
        raise ValueError('Architecture must be x64 or arm64.')
    if config.get('channel') not in ('store', 'development'):
        raise ValueError('Channel must be store or development.')
    if not re.fullmatch(r'[A-Za-z0-9.-]{3,50}', config['identity_name']):
        raise ValueError('Invalid package Identity Name.')
    if not config['publisher'].startswith('CN=') or len(config['publisher']) <= 3:
        raise ValueError('Publisher must be the certificate subject supplied by Partner Center (CN=...).')
    package_version = version_tuple(config['package_version'])
    minimum = version_tuple(config['minimum_windows_version'])
    maximum = version_tuple(config['maximum_tested_windows_version'])
    if maximum < minimum:
        raise ValueError('Maximum tested Windows version must not be below the minimum version.')
    if config['channel'] == 'store':
        if config['identity_name'].casefold() == 'folimeld.dev':
            raise ValueError('The development Identity cannot be used for Store builds.')
        if package_version[0] == 0 or package_version[3] != 0:
            raise ValueError('Store package versions must start above zero and end in .0.')
        if minimum < (10, 0, 22000, 0):
            raise ValueError('This Store release targets Windows 11; minimum build must be at least 22000.')
        for key in ('identity_name', 'publisher', 'publisher_display_name'):
            value = config[key].casefold()
            if any(marker in value for marker in ('<', '>', 'replace', 'placeholder', 'partner center', 'todo')):
                raise ValueError(f'{key} still contains an example placeholder.')
    return config


def load_config(args):
    if args.store:
        if not args.store_config:
            raise ValueError('--store requires --store-config with verified Partner Center identity values.')
        data = json.loads(args.store_config.read_text(encoding='utf-8-sig'))
        if not isinstance(data, dict) or set(data) != CONFIG_KEYS:
            raise ValueError('Store configuration must contain exactly the keys in store-config.example.json.')
        config = {**data, 'channel': 'store', 'architecture': args.architecture}
    else:
        if args.store_config:
            raise ValueError('--store-config requires --store.')
        config = {
            'identity_name': args.identity_name, 'publisher': args.publisher,
            'publisher_display_name': args.publisher_display_name,
            'package_version': args.package_version or '.'.join(map(str, windows_version(__version__))),
            'minimum_windows_version': '10.0.17763.0',
            'maximum_tested_windows_version': '10.0.26100.0',
            'channel': 'development', 'architecture': args.architecture,
        }
    return validate_config(config)


def render_manifest(config):
    replacements = {
        'IDENTITY_NAME': config['identity_name'], 'PUBLISHER': config['publisher'],
        'PUBLISHER_DISPLAY_NAME': config['publisher_display_name'],
        'VERSION': config['package_version'], 'ARCHITECTURE': config['architecture'],
        'MIN_VERSION': config['minimum_windows_version'],
        'MAX_VERSION_TESTED': config['maximum_tested_windows_version'],
    }
    text = (ROOT / 'packaging/msix/AppxManifest.xml.in').read_text(encoding='utf-8')
    for key, value in replacements.items():
        text = text.replace(f'@{key}@', escape(value, quote=True))
    if re.search(r'@[A-Z_]+@', text):
        raise ValueError('The manifest contains unresolved placeholders.')
    ET.fromstring(text)
    return text


def package_manifest(path):
    with ZipFile(path) as archive:
        if len(archive.namelist()) != len(set(archive.namelist())):
            raise ValueError('The package contains duplicate archive entries.')
        return ET.fromstring(archive.read('AppxManifest.xml'))


def compare_previous(config, previous):
    identity = package_manifest(previous).find('p:Identity', NS)
    if identity is None:
        raise ValueError('Previous package has no Identity.')
    if (identity.get('Name'), identity.get('Publisher')) != (config['identity_name'], config['publisher']):
        raise ValueError('Previous package belongs to a different package family.')
    if version_tuple(config['package_version']) <= version_tuple(identity.get('Version')):
        raise ValueError('The new package version must be greater than the previous package version.')


def archive_path(value):
    value = value.replace('\\', '/')
    path = PurePosixPath(value)
    if not value or path.is_absolute() or '..' in path.parts or ':' in value:
        raise ValueError(f'Invalid package-relative path: {value!r}')
    return path.as_posix()


def inspect_package(path, config):
    root = package_manifest(path)
    expected = render_manifest(config)
    # Compare the settings used for the build, not just the filename.
    actual_identity = root.find('p:Identity', NS)
    expected_root = ET.fromstring(expected)
    for xpath in ('p:Identity', 'p:Dependencies/p:TargetDeviceFamily',
                  'p:Applications/p:Application',
                  'p:Applications/p:Application/uap:VisualElements',
                  'p:Applications/p:Application/uap:VisualElements/uap:DefaultTile'):
        actual, required = root.find(xpath, NS), expected_root.find(xpath, NS)
        if actual is None or actual.attrib != required.attrib:
            raise ValueError(f'Package manifest does not match configuration: {xpath}')
    if root.findtext('p:Properties/p:PublisherDisplayName', namespaces=NS) != config['publisher_display_name']:
        raise ValueError('Publisher display name does not match configuration.')
    if root.findtext('p:Properties/p:Logo', namespaces=NS) != expected_root.findtext('p:Properties/p:Logo', namespaces=NS):
        raise ValueError('Store logo is missing or differs from the template.')
    app = root.find('p:Applications/p:Application', NS)
    if app is None or app.get('EntryPoint') != 'Windows.FullTrustApplication':
        raise ValueError('Expected a full-trust desktop application.')
    if root.find("p:Capabilities/rescap:Capability[@Name='runFullTrust']", NS) is None:
        raise ValueError('runFullTrust capability is missing.')
    if root.find(".//uap:FileType[.='.pdf']", NS) is None:
        raise ValueError('PDF file association is missing.')
    executable = archive_path(app.get('Executable', ''))
    if executable != 'Folimeld.exe':
        raise ValueError('The packaged application must launch Folimeld.exe.')
    sizes = {'Logo': (50, 50), 'Square44x44Logo': (44, 44), 'Square150x150Logo': (150, 150),
             'Square71x71Logo': (71, 71), 'Wide310x150Logo': (310, 150), 'Square310x310Logo': (310, 310)}
    with ZipFile(path) as archive:
        if 'LICENSE.txt' not in archive.namelist():
            raise ValueError('LICENSE.txt is missing.')
        with archive.open(executable) as stream:
            header = stream.read(64)
            if len(header) < 64 or header[:2] != b'MZ':
                raise ValueError('The executable has no valid DOS header.')
            stream.seek(struct.unpack_from('<I', header, 60)[0])
            header = stream.read(6)
            machine = {'x64': 0x8664, 'arm64': 0xAA64}[config['architecture']]
            if len(header) != 6 or header[:4] != b'PE\0\0' or struct.unpack_from('<H', header, 4)[0] != machine:
                raise ValueError('The packaged executable architecture does not match the manifest.')
        for element in root.iter():
            assets = [(key, value) for key, value in element.attrib.items() if key in sizes]
            if element.tag == f"{{{NS['p']}}}Logo":
                assets.append(('Logo', element.text or ''))
            for key, value in assets:
                with archive.open(archive_path(value)) as stream:
                    with Image.open(stream) as image:
                        if image.format != 'PNG' or image.size != sizes[key]:
                            raise ValueError(f'Invalid dimensions or format for {value}.')
                        image.verify()
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'static_checks_passed': True, 'package': str(path), 'sha256': digest,
            'identity': actual_identity.attrib, 'channel': config['channel'],
            'requires': ['WACK', 'installed-package acceptance tests', 'Partner Center validation',
                         'privacy and licensing review']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=('prepare', 'check'))
    parser.add_argument('--architecture', choices=('x64', 'arm64'), default='x64')
    parser.add_argument('--store', action='store_true')
    parser.add_argument('--store-config', type=Path)
    parser.add_argument('--identity-name', default='Folimeld.Dev')
    parser.add_argument('--publisher', default='CN=Takuma Yamada')
    parser.add_argument('--publisher-display-name', default='Takuma Yamada')
    parser.add_argument('--package-version')
    parser.add_argument('--previous-package', type=Path)
    parser.add_argument('--output-directory', type=Path, required=True)
    parser.add_argument('--package', type=Path)
    args = parser.parse_args()
    try:
        if args.operation == 'check':
            (args.output_directory / 'preflight.json').unlink(missing_ok=True)
        if args.store and any(value != parser.get_default(name) for name, value in (
            ('identity_name', args.identity_name), ('publisher', args.publisher),
            ('publisher_display_name', args.publisher_display_name), ('package_version', args.package_version))):
            raise ValueError('Store configuration cannot be combined with identity or version overrides.')
        config = load_config(args)
        if args.previous_package:
            compare_previous(config, args.previous_package)
        if args.operation == 'prepare':
            manifest = render_manifest(config)
            args.output_directory.mkdir(parents=True, exist_ok=True)
            (args.output_directory / 'AppxManifest.xml').write_text(manifest, encoding='utf-8')
            report = config
            name = 'config.json'
        else:
            if args.package is None:
                raise ValueError('check requires --package.')
            report = inspect_package(args.package, config)
            args.output_directory.mkdir(parents=True, exist_ok=True)
            name = 'preflight.json'
        (args.output_directory / name).write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
        print(f'{args.operation}: {args.output_directory / name}')
    except (ValueError, OSError, KeyError, ET.ParseError, BadZipFile) as exc:
        parser.exit(1, f'MSIX preflight failed: {exc}\n')


if __name__ == '__main__':
    main()
