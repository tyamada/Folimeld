"""Measure PDF editing and thumbnail cost without modifying an input PDF.

Run from the repository root: python -m tools.benchmark_pdf --pages 100
RSS is sampled every 5 ms and can miss short peaks. Use one process per case.
"""
import argparse
from contextlib import contextmanager
import gc
from importlib.metadata import version
import json
from io import BytesIO
import os
from pathlib import Path
import platform
from tempfile import TemporaryDirectory
from threading import Event, Thread
from time import perf_counter
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import fitz
from PIL import Image
import psutil
from PySide6.QtWidgets import QApplication

from folimeld.app import MainWindow


@contextmanager
def sampled_memory():
    process = psutil.Process()
    baseline = process.memory_info().rss
    samples = [baseline]
    stop = Event()

    def sample():
        while not stop.wait(0.005):
            samples.append(process.memory_info().rss)

    worker = Thread(target=sample, daemon=True)
    worker.start()
    try:
        yield samples, baseline
    finally:
        samples.append(process.memory_info().rss)
        stop.set()
        worker.join()


def create_fixture(path, pages, image_size):
    with fitz.open() as doc:
        for number in range(pages):
            page = doc.new_page()
            page.insert_text((30, 40), str(number))
            if image_size:
                # Distinct, deterministic images prevent PDF stream deduplication.
                image = Image.frombytes("RGB", (image_size, image_size),
                                        bytes((i * 31 + number * 17 + i // 251) % 256
                                              for i in range(image_size * image_size * 3)))
                encoded = BytesIO()
                image.save(encoded, format="PNG", compress_level=0)
                page.insert_image(fitz.Rect(30, 60, 530, 760), stream=encoded.getvalue())
        doc.save(path)


def benchmark(input_path, output_path):
    app = QApplication.instance() or QApplication([])
    with patch("folimeld.app.is_packaged", return_value=False):
        window = MainWindow()
    window.show()
    app.processEvents()
    timings = {}
    max_batch_ms = 0.0
    peak_resident_thumbnails = 0

    def measure(name, operation):
        started = perf_counter()
        result = operation()
        timings[name] = (perf_counter() - started) * 1000
        return result

    def render():
        nonlocal max_batch_ms, peak_resident_thumbnails
        # Explicit ticks avoid mixing scheduled and measured thumbnail batches.
        window._thumbnail_timer.stop()
        while window._pending_thumbnails:
            started = perf_counter()
            window._render_thumbnail_batch()
            max_batch_ms = max(max_batch_ms, (perf_counter() - started) * 1000)
            app.processEvents()
        peak_resident_thumbnails = max(peak_resident_thumbnails, sum(
            not window.pages.item(row).icon().isNull() for row in range(window.pages.count())
        ))

    def scroll_document():
        grid = window.pages.gridSize()
        viewport = window.pages.viewport().size()
        stride = max(1, viewport.width() // grid.width()) * max(1, viewport.height() // grid.height())
        for row in list(range(0, window.pages.count(), stride)) + [window.pages.count() - 1, 0]:
            window.pages.scrollToItem(window.pages.item(row))
            app.processEvents()
            render()

    try:
        gc.collect()
        with sampled_memory() as (samples, baseline):
            measure("open", lambda: window.model.open(str(input_path)))
            measure("refresh", window.refresh)
            measure("initial_thumbnails", render)
            measure("scroll_thumbnails", scroll_document)
            measure("rotate", lambda: window.model.rotate([0], 90))
            measure("refresh_after_rotation", window.refresh)
            measure("rotation_thumbnails", render)
            undo_performed = measure("undo", window.model.undo)
            redo_performed = measure("redo", window.model.redo)
            if window.model.doc.page_count > 1:
                measure("reorder", lambda: window.model.reorder(0, window.model.doc.page_count - 1))
            measure("save", lambda: window.model.save(str(output_path)))
            result = {
                "input_bytes": input_path.stat().st_size,
                "pages": window.model.doc.page_count,
                "thumbnail_size": window.thumbnail_size,
                "milliseconds": timings,
                "max_thumbnail_batch_ms": max_batch_ms,
                "peak_resident_thumbnails": peak_resident_thumbnails,
                "rss_baseline_bytes": baseline,
                "sampled_peak_rss_bytes": max(samples),
                "history_bytes": window.model.history_bytes,
                "undo_performed": undo_performed,
                "redo_performed": redo_performed,
            }
        # The final memory sample is appended when leaving the context.
        result["sampled_peak_rss_bytes"] = max(samples)
        return result
    finally:
        window.model.dirty = False
        window.close()
        window.deleteLater()
        app.processEvents()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, help="Existing PDF; never overwritten")
    parser.add_argument("--pages", type=int, default=100)
    parser.add_argument("--image-size", type=int, default=0, help="RGB image side length per generated page")
    parser.add_argument("--output", type=Path, help="JSON report path")
    args = parser.parse_args()
    if args.pages < 1 or args.image_size < 0:
        parser.error("pages must be positive and image-size must be nonnegative")
    if args.input and args.output and args.input.resolve() == args.output.resolve():
        parser.error("output must differ from input")
    with TemporaryDirectory(prefix="folimeld-benchmark-") as directory:
        root = Path(directory)
        source = args.input or root / "source.pdf"
        if not args.input:
            create_fixture(source, args.pages, args.image_size)
        result = benchmark(source, root / "saved.pdf")
    result["environment"] = {
        "python": platform.python_version(), "platform": platform.platform(),
        "dependencies": {name: version(name) for name in ("PyMuPDF", "PySide6", "Pillow", "psutil")},
    }
    result["fixture"] = {"generated": args.input is None, "image_size": args.image_size if not args.input else None}
    report = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding="utf-8")
    print(report, end="")


if __name__ == "__main__":
    main()
