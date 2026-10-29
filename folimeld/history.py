"""Owned snapshot storage; disk snapshots disappear when closed."""
from tempfile import TemporaryFile
from typing import IO


class Snapshot:
    def __init__(self, data: bytes) -> None:
        self.size = len(data)
        self._data: bytes | None = data
        self._file: IO[bytes] | None = None

    @property
    def in_memory(self) -> bool:
        return self._data is not None

    def spill(self) -> None:
        if self._data is None:
            return
        stream = TemporaryFile(prefix='folimeld-history-')
        try:
            stream.write(self._data)
            stream.flush()
        except BaseException:
            stream.close()
            raise
        self._file = stream
        self._data = None

    def read(self) -> bytes:
        if self._data is not None:
            return self._data
        if self._file is None:
            raise RuntimeError('History snapshot is closed.')
        self._file.seek(0)
        return self._file.read()

    def close(self) -> None:
        if self._file is not None:
            self._file.close()
            self._file = None
        self._data = None
