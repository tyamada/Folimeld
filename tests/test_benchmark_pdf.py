import hashlib
from unittest.mock import patch

import fitz
import pytest

from tools.benchmark_pdf import benchmark, create_fixture, main
from folimeld.model import PdfDocument


@pytest.mark.parametrize("history_limit", [0, 128 * 1024 * 1024])
def test_image_benchmark_keeps_input_unchanged(tmp_path, history_limit):
    source = tmp_path / "source.pdf"
    saved = tmp_path / "saved.pdf"
    create_fixture(source, pages=2, image_size=16)
    original = hashlib.sha256(source.read_bytes()).digest()
    with patch("folimeld.app.PdfDocument", side_effect=lambda: PdfDocument(history_limit)):
        result = benchmark(source, saved)
    assert hashlib.sha256(source.read_bytes()).digest() == original
    assert result["pages"] == 2
    assert result["undo_performed"] is (history_limit > 0)
    assert result["redo_performed"] is (history_limit > 0)
    assert result["sampled_peak_rss_bytes"] >= result["rss_baseline_bytes"] > 0
    assert all(value >= 0 for value in result["milliseconds"].values())
    with fitz.open(saved) as doc:
        assert [int(page.get_text()) for page in doc] == [1, 0]
        assert [page.rotation for page in doc] == [0, 90]
        assert all(page.get_images() for page in doc)


def test_report_cannot_overwrite_input(tmp_path, monkeypatch):
    source = tmp_path / "source.pdf"
    source.write_bytes(b"must be preserved")
    monkeypatch.setattr("sys.argv", ["benchmark_pdf", "--input", str(source), "--output", str(source)])
    with pytest.raises(SystemExit) as error:
        main()
    assert error.value.code == 2
    assert source.read_bytes() == b"must be preserved"
