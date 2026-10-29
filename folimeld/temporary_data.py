"""Authenticated temporary storage; keys are kept separately in process memory."""
import io
import os
import secrets
from typing import IO

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


MAGIC = b'Folimeld-Temp-v1\0'
NONCE_SIZE = 12
TAG_SIZE = 16
OVERHEAD = len(MAGIC) + NONCE_SIZE + TAG_SIZE
CHUNK_SIZE = 1024 * 1024


def new_key() -> bytes:
    return secrets.token_bytes(32)


def _write(stream: IO[bytes], data: bytes) -> None:
    if stream.write(data) != len(data):
        raise OSError('Incomplete encrypted temporary-file write.')


def encrypt_to(stream: IO[bytes], data: bytes, key: bytes) -> None:
    """Write AES-256-GCM ciphertext without writing plaintext to the stream."""
    if len(key) != 32:
        raise ValueError('Temporary encryption requires a 256-bit key.')
    nonce = secrets.token_bytes(NONCE_SIZE)
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce)).encryptor()
    cipher.authenticate_additional_data(MAGIC)
    _write(stream, MAGIC + nonce)
    for start in range(0, len(data), CHUNK_SIZE):
        _write(stream, cipher.update(memoryview(data)[start:start + CHUNK_SIZE]))
    _write(stream, cipher.finalize())
    _write(stream, cipher.tag)
    stream.flush()


def decrypt_from(stream: IO[bytes], key: bytes) -> bytes:
    """Return plaintext only after checking the entire authentication tag."""
    stream.seek(0, os.SEEK_END)
    remaining = stream.tell() - OVERHEAD
    stream.seek(0)
    if remaining < 0 or stream.read(len(MAGIC)) != MAGIC:
        raise OSError('Invalid encrypted temporary-file header.')
    nonce = stream.read(NONCE_SIZE)
    try:
        if len(key) != 32:
            raise ValueError('Temporary encryption requires a 256-bit key.')
        cipher = Cipher(algorithms.AES(key), modes.GCM(nonce)).decryptor()
        cipher.authenticate_additional_data(MAGIC)
        with io.BytesIO() as plaintext:
            while remaining:
                block = stream.read(min(CHUNK_SIZE, remaining))
                if not block:
                    raise OSError('Encrypted temporary file is truncated.')
                plaintext.write(cipher.update(block))
                remaining -= len(block)
            plaintext.write(cipher.finalize_with_tag(stream.read(TAG_SIZE)))
            return plaintext.getvalue()
    except (InvalidTag, ValueError) as exc:
        raise OSError('Encrypted temporary data could not be authenticated.') from exc
