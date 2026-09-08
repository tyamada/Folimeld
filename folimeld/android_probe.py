"""Experimental Qt/Android front end; desktop entry point remains unchanged."""
from pathlib import Path
import sys
import tempfile
from uuid import uuid4

import fitz
from PySide6.QtCore import QFile, QIODevice, Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (
    QApplication, QFileDialog, QHBoxLayout, QLabel, QMainWindow,
    QMessageBox, QPushButton, QScrollArea, QVBoxLayout, QWidget,
)

from folimeld.model import PdfDocument


def copy_file(source: str, destination: str) -> None:
    """Use Qt's file engine, including Android SAF content URIs, in chunks."""
    reader, writer = QFile(source), QFile(destination)
    if not reader.open(QIODevice.OpenModeFlag.ReadOnly):
        raise OSError(reader.errorString())
    try:
        if not writer.open(QIODevice.OpenModeFlag.WriteOnly | QIODevice.OpenModeFlag.Truncate):
            raise OSError(writer.errorString())
        try:
            while not reader.atEnd():
                chunk = reader.read(1024 * 1024)
                if reader.error() != QFile.FileError.NoError:
                    raise OSError(reader.errorString())
                if not chunk:
                    raise OSError("File read made no progress")
                if writer.write(chunk) != len(chunk):
                    raise OSError(writer.errorString())
            if not writer.flush():
                raise OSError(writer.errorString())
        finally:
            writer.close()
    finally:
        reader.close()


class ProbeSession:
    """Keep originals untouched; export a separate PDF through the Qt file API."""

    def __init__(self):
        self.workspace = tempfile.TemporaryDirectory(prefix="folimeld-android-")
        self.pdf = PdfDocument()

    def open(self, uri: str) -> None:
        staged = Path(self.workspace.name) / (uuid4().hex + ".pdf")
        previous = self.pdf.path
        try:
            copy_file(uri, str(staged))
            self.pdf.open(str(staged))
        except Exception:
            staged.unlink(missing_ok=True)
            raise
        if previous is not None:
            previous.unlink(missing_ok=True)

    def export(self, uri: str) -> None:
        # Save a clone so export failure cannot mark the live document clean.
        if not self.pdf.loaded:
            raise ValueError("Open a PDF first")
        snapshot = Path(self.workspace.name) / (uuid4().hex + ".pdf")
        clone = PdfDocument()
        try:
            clone.doc = fitz.open(stream=self.pdf.doc.tobytes(), filetype="pdf")
            clone.save(str(snapshot))
            copy_file(str(snapshot), uri)
            self.pdf.dirty = False
        finally:
            clone.close()
            snapshot.unlink(missing_ok=True)

    def preview(self, index: int) -> QImage:
        page = self.pdf.doc[index]
        scale = min(1.0, 720 / max(page.rect.width, page.rect.height))
        pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale), colorspace=fitz.csRGB, alpha=False)
        return QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format.Format_RGB888).copy()

    def close(self) -> None:
        self.pdf.close()
        self.workspace.cleanup()


class ProbeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.session = ProbeSession()
        self.page = 0
        self.setWindowTitle("Folimeld Android prototype")
        self.resize(800, 700)
        body = QWidget()
        layout = QVBoxLayout(body)
        files = QHBoxLayout()
        self.open_button = QPushButton("Open PDF")
        self.save_button = QPushButton("Export PDF")
        files.addWidget(self.open_button)
        files.addWidget(self.save_button)
        layout.addLayout(files)
        self.status = QLabel("Open a PDF. Password-protected files are not supported in this prototype.")
        self.status.setWordWrap(True)
        layout.addWidget(self.status)
        self.image = QLabel()
        self.image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.image)
        layout.addWidget(scroll)
        navigation = QHBoxLayout()
        self.previous = QPushButton("Previous")
        self.rotate_button = QPushButton("Rotate 90°")
        self.next = QPushButton("Next")
        for button in (self.previous, self.rotate_button, self.next):
            navigation.addWidget(button)
        layout.addLayout(navigation)
        for button in body.findChildren(QPushButton):
            button.setMinimumHeight(48)
        self.setCentralWidget(body)
        self.open_button.clicked.connect(self.open_pdf)
        self.save_button.clicked.connect(self.export_pdf)
        self.previous.clicked.connect(lambda: self.navigate(-1))
        self.next.clicked.connect(lambda: self.navigate(1))
        self.rotate_button.clicked.connect(self.rotate)
        self.refresh()

    def discard_allowed(self) -> bool:
        return not self.session.pdf.dirty or QMessageBox.question(
            self, "Unsaved changes", "Discard changes that have not been exported?"
        ) == QMessageBox.StandardButton.Yes

    def open_pdf(self):
        if not self.discard_allowed():
            return
        path, _ = QFileDialog.getOpenFileName(self, "Open PDF", "", "PDF (*.pdf)")
        if not path:
            return
        try:
            self.session.open(path)
            self.page = 0
            self.refresh()
        except Exception as error:
            QMessageBox.warning(self, "Cannot open PDF", str(error) or "A password is required.")

    def export_pdf(self):
        path, _ = QFileDialog.getSaveFileName(self, "Export PDF", "folimeld-export.pdf", "PDF (*.pdf)")
        if not path:
            return
        try:
            self.session.export(path)
            self.refresh()
            self.status.setText(self.status.text() + " — Exported")
        except Exception as error:
            QMessageBox.warning(self, "Export failed", str(error))

    def navigate(self, delta):
        self.page += delta
        self.refresh()

    def rotate(self):
        self.session.pdf.rotate([self.page], 90)
        self.refresh()

    def refresh(self):
        loaded = self.session.pdf.loaded
        count = self.session.pdf.doc.page_count if loaded else 0
        self.save_button.setEnabled(count > 0)
        self.rotate_button.setEnabled(count > 0)
        self.previous.setEnabled(count > 0 and self.page > 0)
        self.next.setEnabled(count > 0 and self.page < count - 1)
        if count:
            self.image.setPixmap(QPixmap.fromImage(self.session.preview(self.page)))
            self.status.setText(f"Page {self.page + 1} / {count}" + (" — Modified" if self.session.pdf.dirty else ""))
        else:
            self.image.clear()

    def closeEvent(self, event):
        if not self.discard_allowed():
            event.ignore()
            return
        self.session.close()
        event.accept()


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Folimeld Android prototype")
    window = ProbeWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
