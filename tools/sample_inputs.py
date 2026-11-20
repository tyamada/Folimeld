"""Opt-in, hash-verified real PDF inputs for integration/GUI verification."""
import argparse
import hashlib
import os
from pathlib import Path
from threading import Event

from folimeld.sample_catalogue import download_sample, parse_catalogue, verified

REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_URL = 'https://github.com/tyamada/manga-prompt-kit/releases/download/manga-pdf-20261103-v1/pdf-manifest.json'
MANIFEST_SHA256 = '4ffcdc152b18fe631b7db4f749907caa1ccf5888511137784d23774abf5d7ed4'


def pinned_entries():
    raw = (Path(__file__).parent / 'data/sample-inputs-v1.json').read_bytes()
    if hashlib.sha256(raw).hexdigest() != MANIFEST_SHA256:
        raise ValueError('Pinned sample input manifest changed.')
    return parse_catalogue(raw)


def default_cache():
    if os.name == 'nt' and os.environ.get('LOCALAPPDATA'):
        return Path(os.environ['LOCALAPPDATA']) / 'Folimeld-Verification/sample-inputs-v1'
    return Path(os.environ.get('XDG_CACHE_HOME', str(Path.home() / '.cache'))) / 'Folimeld-Verification/sample-inputs-v1'


def external_directory(path):
    path = Path(path).expanduser().resolve()
    if path.is_relative_to(REPO_ROOT.resolve()):
        raise ValueError('Use an input/cache directory outside the repository.')
    return path


def resolve_sample_input(sample_id='ep3_ja', *, input_dir=None, cache_dir=None, download=False):
    # Keep the app's IDs unchanged; accept the historical Filipino alias here.
    if sample_id.endswith('_tl'):
        sample_id = sample_id[:-3] + '_fil'
    entries = pinned_entries()
    entry = next((e for e in entries if e['sample_id'] == sample_id), None)
    if entry is None:
        raise ValueError('Unknown pinned sample ID: ' + sample_id)
    cancel = Event()
    if input_dir is not None:
        folder = external_directory(input_dir)
        for candidate in (folder / entry['filename'], folder / (entry['sha256'] + '.pdf')):
            if candidate.exists():
                if not verified(candidate, entry, cancel):
                    raise ValueError('Input PDF size or SHA-256 mismatch: ' + str(candidate))
                return candidate
        raise FileNotFoundError('Verified input PDF not found in --input-dir.')
    cache = external_directory(cache_dir or default_cache())
    original = cache / 'originals' / (entry['sha256'] + '.pdf')
    if verified(original, entry, cancel):
        return original
    if not download:
        raise FileNotFoundError('Prepare the required input first: python -m tools.sample_inputs --sample-id '
                                + sample_id + ' --cache-dir "' + str(cache) + '" --download')
    return download_sample(cache, entry, cancel)


def add_input_arguments(parser):
    parser.add_argument('--input-dir', type=Path, help='External folder containing the verified PDF')
    parser.add_argument('--cache-dir', type=Path, help='External verification cache, separate from app/user PDFs')
    parser.add_argument('--download', action='store_true', help='Explicitly download only the required fixed-release PDF')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sample-id', default='ep3_ja')
    add_input_arguments(parser)
    args = parser.parse_args()
    print(resolve_sample_input(args.sample_id, input_dir=args.input_dir,
                               cache_dir=args.cache_dir, download=args.download))


if __name__ == '__main__':
    main()
