import multiprocessing
import tempfile
from datetime import datetime
from pathlib import Path

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (QAbstractItemView, QComboBox, QDialog, QDialogButtonBox,
                               QHBoxLayout, QHeaderView, QLabel, QMessageBox,
                               QProgressDialog, QPushButton, QTableWidget,
                               QTableWidgetItem, QVBoxLayout)

from .image_import import conversion_worker, sort_entries


class ImageImportDialog(QDialog):
    def __init__(self, entries, tr, parent=None):
        super().__init__(parent)
        self.tr = tr
        self.entries = entries
        self.setWindowTitle(tr('import_images'))
        self.resize(800, 500)
        layout = QVBoxLayout(self)
        controls = QHBoxLayout()
        self.sort = QComboBox()
        for key, field in [('filename', 'name'), ('image_created', 'created'), ('image_modified', 'modified')]:
            self.sort.addItem(tr(key), field)
        self.direction = QComboBox()
        self.direction.addItems([tr('image_ascending'), tr('image_descending')])
        self.size = QComboBox()
        self.size.addItem(tr('image_original_size'), 'image')
        self.size.addItem('A4', 'a4')
        for key, widget in [('image_sort', self.sort), ('image_direction', self.direction), ('image_page_size', self.size)]:
            controls.addWidget(QLabel(tr(key)))
            controls.addWidget(widget)
        layout.addLayout(controls)
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels([tr('filename'), tr('image_created'), tr('image_modified')])
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)
        remove = QPushButton(tr('image_exclude'))
        remove.clicked.connect(self.exclude)
        layout.addWidget(remove)
        self.count = QLabel()
        layout.addWidget(self.count)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.start = buttons.button(QDialogButtonBox.StandardButton.Ok)
        self.start.setText(tr('image_load'))
        buttons.button(QDialogButtonBox.StandardButton.Cancel).setText(tr('cancel'))
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        self.sort.currentIndexChanged.connect(self.refresh)
        self.direction.currentIndexChanged.connect(self.refresh)
        self.refresh()

    def refresh(self):
        self.entries = sort_entries(self.entries, self.sort.currentData(), self.direction.currentIndex() == 1)
        self.table.setRowCount(len(self.entries))
        for row, entry in enumerate(self.entries):
            values = [entry.path.name]
            for timestamp in (entry.created, entry.modified):
                values.append(datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                              if timestamp is not None else self.tr('image_unavailable'))
            for column, value in enumerate(values):
                self.table.setItem(row, column, QTableWidgetItem(value))
        self.count.setText(self.tr('image_count', count=len(self.entries)))
        self.start.setEnabled(bool(self.entries))

    def exclude(self):
        rows = {item.row() for item in self.table.selectionModel().selectedRows()}
        self.entries = [entry for row, entry in enumerate(self.entries) if row not in rows]
        self.refresh()

    def convert(self, model):
        """Poll a spawned worker without sharing PyMuPDF objects with the UI."""
        with tempfile.TemporaryDirectory(prefix='folimeld-images-') as directory:
            destination = Path(directory) / 'images.pdf'
            context = multiprocessing.get_context('spawn')
            receiver, sender = context.Pipe(duplex=False)
            process = context.Process(target=conversion_worker,
                                      args=([str(e.path) for e in self.entries], str(destination),
                                            self.size.currentData(), sender))
            progress = QProgressDialog(self.tr('image_converting'), self.tr('cancel'), 0, len(self.entries), self)
            progress.setWindowTitle(self.tr('import_images'))
            progress.setAutoClose(False)
            progress.setAutoReset(False)
            result = []
            timer = QTimer(progress)

            def poll():
                try:
                    while receiver.poll():
                        kind, value = receiver.recv()
                        if kind == 'progress':
                            progress.setValue(value)
                        else:
                            result.append((kind, value))
                            progress.accept()
                            return
                except EOFError:
                    pass
                if not process.is_alive() and not result:
                    result.append(('error', self.tr('image_worker_failed')))
                    progress.accept()

            try:
                process.start()
                sender.close()
                timer.timeout.connect(poll)
                timer.start(50)
                progress.exec()
                timer.stop()
                if process.is_alive():
                    process.terminate()
                process.join()
                if progress.wasCanceled() or not result:
                    return False
                if result[0][0] == 'error':
                    QMessageBox.warning(self, self.tr('error'), str(result[0][1]))
                    return False
                model.open_generated(str(destination))
                return True
            finally:
                timer.stop()
                if process.pid is not None:
                    if process.is_alive():
                        process.terminate()
                    process.join()
                receiver.close()
                sender.close()
