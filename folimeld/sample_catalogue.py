"""Validated, persistent sample catalogue and verified per-book downloads."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
from threading import Event
from urllib.parse import urlsplit, unquote
from urllib.request import Request, HTTPRedirectHandler, build_opener
from uuid import uuid4

from .sample_catalogue_data import BUNDLED_CATALOGUE

CATALOGUE_URL = 'https://raw.githubusercontent.com/tyamada/manga-prompt-kit/main/releases/pdf-manifest.json'
RELEASE_URL = 'https://github.com/tyamada/manga-prompt-kit/releases/tag/manga-pdf-20261103-v1'
LICENSE_URL = 'https://creativecommons.org/licenses/by/4.0/'
AUTHOR = 'こまいろ日和 / Komairo Hiyori'
MAX_CATALOGUE_BYTES = 2 * 1024 * 1024
MAX_PDF_BYTES = 256 * 1024 * 1024


class Cancelled(Exception):
    pass


def validate_url(url: str, *, redirect: bool = False) -> str:
    if not isinstance(url, str) or any(c.isspace() or ord(c) < 32 for c in url):
        raise ValueError('Invalid sample URL.')
    p = urlsplit(url)
    if (p.scheme != 'https' or p.username or p.password or p.fragment
            or p.port not in (None, 443) or '\\' in url):
        raise ValueError('Only approved HTTPS sample URLs are supported.')
    if url == CATALOGUE_URL:
        return url
    if p.hostname == 'github.com' and not p.query:
        if re.fullmatch(r'/tyamada/manga-prompt-kit/releases/download/(?!latest/)[A-Za-z0-9][A-Za-z0-9._-]*/[A-Za-z0-9][A-Za-z0-9._-]*\.pdf', p.path):
            return url
    if redirect and p.hostname in {'release-assets.githubusercontent.com', 'objects.githubusercontent.com'}:
        if p.path.startswith(('/github-production-release-asset/', '/github-production-release-asset-')) and '..' not in unquote(p.path).split('/'):
            return url
    raise ValueError('Unapproved sample download source.')


class _Redirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        validate_url(newurl, redirect=True)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def open_url(url):
    validate_url(url)
    response = build_opener(_Redirect()).open(Request(url, headers={'User-Agent': 'Folimeld-samples/1', 'Accept-Encoding': 'identity'}), timeout=15)
    try:
        validate_url(response.geturl(), redirect=True)
        if response.status != 200:
            raise OSError('Unexpected download response.')
    except Exception:
        response.close()
        raise
    return response


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Duplicate JSON field.')
        result[key] = value
    return result


def parse_catalogue(raw: bytes) -> list[dict]:
    if len(raw) > MAX_CATALOGUE_BYTES:
        raise ValueError('Sample catalogue is too large.')
    data = json.loads(raw, object_pairs_hook=_unique_object)
    if not isinstance(data, dict) or type(data.get('schema_version')) is not int or data['schema_version'] != 1:
        raise ValueError('Unsupported sample catalogue schema.')
    entries = data.get('entries')
    if not isinstance(entries, list) or not 1 <= len(entries) <= 2000:
        raise ValueError('Invalid sample entries.')
    ids, combinations, names = set(), set(), set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError('Invalid sample entry.')
        for key in ('sample_id', 'language_key', 'locale', 'title', 'filename', 'sha256', 'license', 'new_download_url'):
            value = entry.get(key)
            if not isinstance(value, str) or not value or len(value) > 2048 or any(ord(c) < 32 for c in value):
                raise ValueError('Missing or invalid sample metadata: ' + key)
        if not re.fullmatch(r'[A-Za-z0-9_-]+', entry['sample_id']):
            raise ValueError('Invalid sample ID.')
        if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]*\.pdf', entry['filename']):
            raise ValueError('Invalid sample filename.')
        if not re.fullmatch(r'[a-fA-F0-9]{64}', entry['sha256']) or entry['license'] != 'CC-BY-4.0':
            raise ValueError('Invalid sample digest or license.')
        for key, limit in [('episode', 10000), ('pages', 10000), ('bytes', MAX_PDF_BYTES)]:
            if type(entry.get(key)) is not int or not 0 < entry[key] <= limit:
                raise ValueError('Invalid sample size or episode.')
        validate_url(entry['new_download_url'])
        if urlsplit(entry['new_download_url']).path.rsplit('/', 1)[-1] != entry['filename']:
            raise ValueError('Sample filename and URL differ.')
        combination = (entry['episode'], entry['language_key'], entry['locale'])
        if entry['sample_id'] in ids or combination in combinations or entry['filename'].lower() in names:
            raise ValueError('Duplicate sample ID, locale/episode or filename.')
        ids.add(entry['sample_id']); combinations.add(combination); names.add(entry['filename'].lower())
    return entries


def _check_cancel(cancel):
    if cancel.is_set():
        raise Cancelled()


def _read_catalogue(cancel):
    chunks, length = [], 0
    with open_url(CATALOGUE_URL) as response:
        while True:
            _check_cancel(cancel)
            block = getattr(response, 'read1', response.read)(65536)
            if not block:
                return b''.join(chunks)
            length += len(block)
            if length > MAX_CATALOGUE_BYTES:
                raise ValueError('Sample catalogue is too large.')
            chunks.append(block)


def load_catalogue(root: Path, cancel: Event) -> tuple[list[dict], str]:
    cache = root / 'catalogue-v1.json'
    try:
        raw = _read_catalogue(cancel)
        entries = parse_catalogue(raw)
        _check_cancel(cancel)
        root.mkdir(parents=True, exist_ok=True)
        temp = root / (uuid4().hex + '.catalogue.part')
        try:
            temp.write_bytes(raw)
            os.replace(temp, cache)
        finally:
            temp.unlink(missing_ok=True)
        return entries, 'online'
    except Cancelled:
        raise
    except Exception:
        try:
            with cache.open('rb') as stream:
                return parse_catalogue(stream.read(MAX_CATALOGUE_BYTES + 1)), 'cached'
        except Exception:
            return parse_catalogue(BUNDLED_CATALOGUE.encode('utf-8')), 'bundled'


def verified(path: Path, entry: dict, cancel: Event) -> bool:
    try:
        if path.is_symlink() or path.stat().st_size != entry['bytes']:
            return False
        digest = hashlib.sha256()
        with path.open('rb') as stream:
            if stream.read(5) != b'%PDF-':
                return False
            stream.seek(0)
            while block := stream.read(1024 * 1024):
                _check_cancel(cancel)
                digest.update(block)
        return digest.hexdigest() == entry['sha256'].lower()
    except OSError:
        return False


def download_sample(root: Path, entry: dict, cancel: Event, progress=lambda done, total: None) -> Path:
    # Revalidate even when called without the UI/catalogue loader.
    parse_catalogue(json.dumps({'schema_version': 1, 'entries': [entry]}).encode())
    folder = root / 'originals'
    folder.mkdir(parents=True, exist_ok=True)
    destination = folder / (entry['sha256'].lower() + '.pdf')
    _check_cancel(cancel)
    if verified(destination, entry, cancel):
        progress(entry['bytes'], entry['bytes'])
        return destination
    temp = folder / (uuid4().hex + '.part')
    try:
        done, digest, prefix = 0, hashlib.sha256(), b''
        with open_url(entry['new_download_url']) as response, temp.open('xb') as stream:
            length = response.headers.get('Content-Length')
            if length is not None and int(length) != entry['bytes']:
                raise ValueError('Sample download size differs from catalogue.')
            while True:
                _check_cancel(cancel)
                block = getattr(response, 'read1', response.read)(65536)
                if not block:
                    break
                done += len(block)
                if done > entry['bytes']:
                    raise ValueError('Sample download exceeds expected size.')
                prefix = (prefix + block)[:5]
                stream.write(block); digest.update(block)
                progress(done, entry['bytes'])
            stream.flush(); os.fsync(stream.fileno())
        _check_cancel(cancel)
        if done != entry['bytes'] or digest.hexdigest() != entry['sha256'].lower() or prefix != b'%PDF-':
            raise ValueError('Sample PDF size, signature or SHA-256 mismatch.')
        if destination.exists() and not verified(destination, entry, cancel):
            destination.rename(folder / (destination.name + '.corrupt-' + uuid4().hex))
        os.replace(temp, destination)
        return destination
    finally:
        temp.unlink(missing_ok=True)


def working_copy(root: Path, original: Path, entry: dict, cancel: Event) -> Path:
    """Never let Save overwrite the verified offline original."""
    if not verified(original, entry, cancel):
        raise ValueError('Cached sample failed verification.')
    destination = root / 'opened' / uuid4().hex / entry['filename']
    destination.parent.mkdir(parents=True, exist_ok=False)
    with original.open('rb') as src, destination.open('xb') as dst:
        while block := src.read(1024 * 1024):
            dst.write(block)
    return destination
