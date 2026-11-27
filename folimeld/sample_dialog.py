"""Nonmodal sample browser with cancellable background I/O."""
from html import escape
from pathlib import Path
from threading import Event

from PySide6.QtCore import QLocale, QThread, Signal, QStandardPaths, Qt
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                              QPushButton, QTreeWidget, QTreeWidgetItem, QProgressBar, QComboBox)

from .sample_catalogue import (AUTHOR, SOURCE_PAGE_URL, LICENSE_URL, Cancelled,
                               load_catalogue, download_sample, working_copy)


def sample_source_page(language: str | None) -> str:
    """Use only known published language pages; never interpolate arbitrary input."""
    locale = (language or '').replace('_', '-').lower()
    chinese = {'zh': 'zh-Hans', 'zh-cn': 'zh-Hans', 'zh-sg': 'zh-Hans',
               'zh-hans': 'zh-Hans', 'zh-tw': 'zh-Hant', 'zh-hk': 'zh-Hant',
               'zh-hant': 'zh-Hant'}
    page = chinese.get(locale)
    if page is None:
        base = locale.split('-')[0]
        page = base if base in {'ja', 'en', 'ko', 'de', 'fr', 'es', 'pt',
                               'vi', 'fil', 'ne', 'id', 'it'} else ''
    return SOURCE_PAGE_URL + page + '/' if page else SOURCE_PAGE_URL


class SampleWorker(QThread):
    result = Signal(object)
    failed = Signal(str)
    progress = Signal(int, int)

    def __init__(self, root, entry, parent):
        super().__init__(parent)
        self.root, self.entry = root, entry
        self.cancel = Event()

    def run(self):
        try:
            if self.entry is None:
                self.result.emit(load_catalogue(self.root, self.cancel))
            else:
                original = download_sample(self.root, self.entry, self.cancel,
                                           self.progress.emit)
                self.result.emit(working_copy(self.root, original, self.entry, self.cancel))
        except Cancelled:
            self.failed.emit('')
        except Exception:
            # Do not expose signed redirect URLs, paths or internal errors.
            self.failed.emit('download')


class SampleDialog(QDialog):
    selected = Signal(str)

    def __init__(self, tr, parent=None, root=None, language=None):
        super().__init__(parent)
        self.tr_ = tr
        self.preferred_language = language or getattr(getattr(tr, "__self__", None), "language", None)
        self._filter_initialized = False
        self.root = Path(root) if root is not None else Path(QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.AppLocalDataLocation)) / 'samples-v1'
        self.worker = None
        self.entries = []
        self.loaded = False
        self.setWindowTitle(tr('samples'))
        self.setWindowModality(Qt.WindowModality.NonModal)
        self.resize(820, 520)
        layout = QVBoxLayout(self)
        self.notice = QLabel(tr('samples_intro'))
        self.notice.setWordWrap(True)
        layout.addWidget(self.notice)
        controls = QHBoxLayout()
        self.language_filter = QComboBox(self)
        self.language_filter.setObjectName('sample_language_filter')
        self.language_filter.addItem(tr('sample_all_languages'), '')
        language_label = QLabel(tr('sample_language_filter'))
        language_label.setBuddy(self.language_filter)
        controls.addWidget(language_label)
        controls.addWidget(self.language_filter, 1)
        self.episode_order = QComboBox(self)
        self.episode_order.setObjectName('sample_episode_order')
        self.episode_order.addItem(tr('sample_latest_first'), 'latest')
        self.episode_order.addItem(tr('sample_first_first'), 'first')
        order_label = QLabel(tr('sample_order'))
        order_label.setBuddy(self.episode_order)
        controls.addWidget(order_label)
        controls.addWidget(self.episode_order)
        layout.addLayout(controls)
        self.tree = QTreeWidget(self)
        self.tree.setHeaderLabels([tr('sample_episode'), tr('sample_language'), tr('title'), tr('sample_size')])
        self.tree.setRootIsDecorated(False)
        self.tree.setSortingEnabled(False)
        self.language_filter.currentIndexChanged.connect(self._render_entries)
        self.episode_order.currentIndexChanged.connect(self._render_entries)
        self.tree.itemSelectionChanged.connect(self._selection_changed)
        layout.addWidget(self.tree)
        self.status = QLabel(tr('samples_loading'))
        self.status.setTextFormat(Qt.TextFormat.PlainText)
        self.status.setWordWrap(True)
        layout.addWidget(self.status)
        self.progress = QProgressBar(self)
        self.progress.setRange(0, 100)
        layout.addWidget(self.progress)
        buttons = QHBoxLayout()
        self.refresh_button = QPushButton(tr('samples_refresh'))
        self.open_button = QPushButton(tr('sample_download_open'))
        self.cancel_button = QPushButton(tr('cancel'))
        self.close_button = QPushButton(tr('close_pdf'))
        self.refresh_button.clicked.connect(self.refresh_catalogue)
        self.open_button.clicked.connect(self.open_selected)
        self.cancel_button.clicked.connect(self.cancel_work)
        self.close_button.clicked.connect(self.close)
        for button in (self.refresh_button, self.open_button, self.cancel_button, self.close_button):
            buttons.addWidget(button)
        layout.addLayout(buttons)
        self.copyright_notice = QLabel(tr('sample_copyright', author=AUTHOR))
        self.copyright_notice.setTextFormat(Qt.TextFormat.PlainText)
        self.copyright_notice.setWordWrap(True)
        layout.addWidget(self.copyright_notice)
        self.license_notice = QLabel(
            escape(tr('sample_license')) + ' <a href="' + LICENSE_URL +
            '">Creative Commons Attribution 4.0 International (CC BY 4.0)</a>' +
            ' · <a href="' + sample_source_page(
                self.preferred_language or QLocale.system().name()) + '">' + escape(tr('sample_source')) + '</a>')
        self.license_notice.setOpenExternalLinks(True)
        self.license_notice.setWordWrap(True)
        layout.addWidget(self.license_notice)
        self._set_busy(False)

    def _default_language(self, options):
        system_locale = QLocale.system().bcp47Name().lower()
        preferred = (self.preferred_language or system_locale).replace('_', '-').lower()
        candidates = [(key, locale) for key, locale in options
                      if locale.lower().split('-')[0] == preferred.split('-')[0]]
        for key, locale in candidates:
            if (locale.lower() == preferred
                    or (key.replace('_', '-').lower() == preferred and '-' in preferred)):
                return key
        for key, locale in candidates:
            if QLocale(locale).bcp47Name().lower() == preferred:
                return key
        if '-' not in preferred:
            for key, locale in candidates:
                if QLocale(locale).bcp47Name().lower() == system_locale:
                    return key
        for key, locale in candidates:
            if key.lower() == preferred:
                return key
        return candidates[0][0] if candidates else ''

    def _update_languages(self):
        previous = self.language_filter.currentData()
        options = sorted({(entry['language_key'], entry['locale']) for entry in self.entries})
        selected = previous if self._filter_initialized else self._default_language(options)
        self.language_filter.blockSignals(True)
        try:
            self.language_filter.clear()
            self.language_filter.addItem(self.tr_('sample_all_languages'), '')
            for key, locale in options:
                native = QLocale(locale).nativeLanguageName() or key
                self.language_filter.addItem(f'{native} / {locale}', key)
            self.language_filter.setCurrentIndex(max(0, self.language_filter.findData(selected)))
        finally:
            self.language_filter.blockSignals(False)
        self._filter_initialized = True

    def _render_entries(self):
        selected = self.tree.selectedItems()
        selected_id = selected[0].data(0, Qt.ItemDataRole.UserRole)['sample_id'] if selected else None
        language = self.language_filter.currentData()
        latest = self.episode_order.currentData() == 'latest'
        entries = [entry for entry in self.entries
                   if not language or entry['language_key'] == language]
        entries.sort(key=lambda entry: (
            -entry['episode'] if latest else entry['episode'],
            entry['locale'], entry['title'], entry['sample_id']))
        self.tree.clear()
        for entry in entries:
            item = QTreeWidgetItem([str(entry['episode']),
                f"{entry['language_key']} / {entry['locale']}", entry['title'],
                f"{entry['bytes'] / 1048576:.1f} MiB"])
            item.setData(0, Qt.ItemDataRole.UserRole, entry)
            self.tree.addTopLevelItem(item)
            if entry['sample_id'] == selected_id:
                item.setSelected(True)
        for column in (0, 1, 2):
            self.tree.resizeColumnToContents(column)
        self._selection_changed()

    def _selection_changed(self):
        self.open_button.setEnabled(self.worker is None and bool(self.tree.selectedItems()))

    def _set_busy(self, busy):
        self.tree.setEnabled(not busy)
        self.language_filter.setEnabled(not busy)
        self.episode_order.setEnabled(not busy)
        self.refresh_button.setEnabled(not busy)
        self.cancel_button.setEnabled(busy)
        self.open_button.setEnabled(not busy and bool(self.tree.selectedItems()))

    def _start(self, entry):
        if self.worker is not None:
            return
        self.worker = SampleWorker(self.root, entry, self)
        self._set_busy(True)
        self.progress.setRange(0, 0 if entry is None else 100)
        self.progress.setValue(0)
        self.worker.progress.connect(self._progress)
        self.worker.result.connect(self._result)
        self.worker.failed.connect(self._failed)
        self.worker.finished.connect(self._finished)
        self.worker.start()

    def refresh_catalogue(self):
        self.status.setText(self.tr_('samples_loading'))
        self._start(None)

    def open_selected(self):
        items = self.tree.selectedItems()
        if not items or self.worker is not None:
            return
        entry = items[0].data(0, Qt.ItemDataRole.UserRole)
        self.status.setText(self.tr_('sample_downloading', title=entry['title']))
        self._start(entry)

    def _progress(self, done, total):
        self.progress.setValue(done * 100 // total)
        self.status.setText(self.tr_('sample_progress', done=f'{done / 1048576:.1f}', total=f'{total / 1048576:.1f}'))

    def _result(self, result):
        if self.worker.cancel.is_set():
            return
        if isinstance(result, tuple):
            self.entries, source = result
            self.loaded = True
            self._update_languages()
            self._render_entries()
            self.status.setText(self.tr_('samples_' + source))
        else:
            self.status.setText(self.tr_('sample_ready'))
            self.selected.emit(str(result))

    def _failed(self, error):
        self.status.setText(self.tr_('sample_failed' if error else 'sample_cancelled'))

    def _finished(self):
        worker, self.worker = self.worker, None
        worker.deleteLater()
        self.progress.setRange(0, 100)
        self._set_busy(False)

    def cancel_work(self):
        if self.worker is not None:
            self.worker.cancel.set()
            self.status.setText(self.tr_('sample_cancelling'))

    def reject(self):
        self.cancel_work()
        super().reject()

    def closeEvent(self, event):
        self.cancel_work()
        super().closeEvent(event)
