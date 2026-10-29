"""Owned snapshot storage; disk snapshots disappear when closed."""
from tempfile import TemporaryFile
from typing import IO

from .temporary_data import OVERHEAD, decrypt_from, encrypt_to, new_key


class Snapshot:
    def __init__(self, data: bytes) -> None:
        self.size = len(data)
        self._data: bytes | None = data
        self._file: IO[bytes] | None = None
        self._key: bytes | None = None

    @property
    def in_memory(self) -> bool:
        return self._data is not None

    @property
    def encrypted_size(self) -> int:
        return self.size + OVERHEAD

    @property
    def disk_size(self) -> int:
        return self.encrypted_size if self._file is not None else 0

    def spill(self) -> None:
        if self._data is None:
            return
        stream = TemporaryFile(prefix='folimeld-history-')
        try:
            key = new_key()
            encrypt_to(stream, self._data, key)
        except BaseException:
            stream.close()
            raise
        self._file = stream
        self._key = key
        self._data = None

    def read(self) -> bytes:
        if self._data is not None:
            return self._data
        if self._file is None or self._key is None:
            raise RuntimeError('History snapshot is closed.')
        return decrypt_from(self._file, self._key)

    def close(self) -> None:
        try:
            if self._file is not None:
                self._file.close()
        finally:
            self._file = None
            self._key = None
            self._data = None
