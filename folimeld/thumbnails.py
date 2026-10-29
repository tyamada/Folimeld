"""Thumbnail reuse, viewport cache and rendering lifecycle, owned by the view."""
from time import perf_counter

import fitz
from PySide6.QtCore import QEvent, QObject, QTimer, Qt
from PySide6.QtGui import QIcon, QImage, QPixmap
from PySide6.QtWidgets import QListWidgetItem

THUMBNAIL_CACHE_LIMIT = 64


class ThumbnailController(QObject):
    def __init__(self, pages, get_document, get_size, page_label, on_error):
        super().__init__(pages)
        self.pages = pages
        self.viewport = pages.viewport()
        self.get_document = get_document
        self.get_size = get_size
        self.page_label = page_label
        self.on_error = on_error
        self.document = None
        self.pending = {}
        self.resident = {}
        self.paused = False
        self.viewport_timer = QTimer(self)
        self.viewport_timer.setSingleShot(True)
        self.viewport_timer.timeout.connect(self.update_viewport)
        self.viewport.installEventFilter(self)
        for scrollbar in (pages.verticalScrollBar(), pages.horizontalScrollBar()):
            scrollbar.valueChanged.connect(lambda _value: self.viewport_timer.start(0))
        self.timer = QTimer(self)
        self.timer.setInterval(1)
        self.timer.timeout.connect(self.render_batch)

    def pause(self):
        self.paused = True
        self.timer.stop()
        self.viewport_timer.stop()

    def resume(self):
        self.paused = False
        self.update_viewport()

    def clear(self):
        self.pause()
        self.pending.clear()
        self.resident.clear()
        self.document = None

    def render_icon(self, page: fitz.Page) -> QIcon:
        rect = page.rect
        scale = min(self.get_size() / rect.width, self.get_size() / rect.height)
        pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
        image = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format.Format_RGB888).copy()
        return QIcon(QPixmap.fromImage(image))

    def refresh(self, selection: list[int] | None = None,
                preserve_scroll: bool = False) -> None:
        scroll_position = self.pages.verticalScrollBar().value()
        self.timer.stop()
        self.pending.clear()
        reusable = {}
        self.pages.blockSignals(True)
        while self.pages.count():
            item = self.pages.takeItem(self.pages.count() - 1)
            if self.document is self.get_document():
                reusable[item.data(Qt.ItemDataRole.UserRole)] = item
        self.document = self.get_document()
        if self.get_document():
            for index, page in enumerate(self.get_document()):
                key = (page.xref, page.rotation, self.get_size())
                item = reusable.pop(key, None)
                if item is None:
                    item = QListWidgetItem()
                item.setText(self.page_label(index + 1))
                item.setTextAlignment(Qt.AlignmentFlag.AlignHCenter)
                item.setData(Qt.ItemDataRole.UserRole, key)
                item.setSelected(False)
                self.pages.addItem(item)
                if item.icon().isNull():
                    self.pending[index] = item
            for row in selection or []:
                if 0 <= row < self.pages.count(): self.pages.item(row).setSelected(True)
        self.pages.blockSignals(False)
        self.pages.doItemsLayout()
        if preserve_scroll:
            self.pages.verticalScrollBar().setValue(scroll_position)
        self.resident = {
            row: self.pages.item(row) for row in range(self.pages.count())
            if not self.pages.item(row).icon().isNull()
        }
        self.update_viewport()

    def eventFilter(self, watched, event) -> bool:
        if watched is self.viewport and event.type() in (QEvent.Type.Resize, QEvent.Type.Show):
            self.viewport_timer.start(0)
        return super().eventFilter(watched, event)

    def rows_in_rect(self, area):
        # Fixed grid rows are ordered vertically. Skip off-screen rows using
        # binary search instead of asking Qt for every page on each scroll.
        low, high = 0, self.pages.count()
        while low < high:
            middle = (low + high) // 2
            if self.pages.visualItemRect(self.pages.item(middle)).bottom() < area.top():
                low = middle + 1
            else:
                high = middle
        for row in range(low, self.pages.count()):
            rect = self.pages.visualItemRect(self.pages.item(row))
            if rect.top() > area.bottom():
                break
            if rect.intersects(area):
                yield row, rect

    def update_viewport(self) -> None:
        self.viewport_timer.stop()
        if self.paused:
            return
        if self.document is not self.get_document() or self.get_document() is None:
            self.timer.stop()
            self.pending.clear()
            return
        count = self.pages.count()
        if count <= THUMBNAIL_CACHE_LIMIT:
            targets = set(range(count))
        else:
            viewport = self.pages.viewport().rect()
            nearby = viewport.adjusted(0, -viewport.height(), 0, viewport.height())
            visible = set()
            neighbors = []
            for row, rect in self.rows_in_rect(nearby):
                if rect.intersects(viewport):
                    visible.add(row)
                elif rect.intersects(nearby):
                    neighbors.append((abs(rect.center().y() - viewport.center().y()), row))
            # Always retain every visible page, even on exceptionally large screens.
            neighbors.sort()
            targets = visible | {row for _, row in neighbors[:max(0, THUMBNAIL_CACHE_LIMIT - len(visible))]}
        for row in list(self.resident):
            if row not in targets:
                self.resident.pop(row).setIcon(QIcon())
        self.pending = {
            row: self.pages.item(row) for row in sorted(targets)
            if self.pages.item(row).icon().isNull()
        }
        if self.pending:
            self.timer.start()
        else:
            self.timer.stop()

    def render_batch(self) -> None:
        if self.paused:
            return
        if self.document is not self.get_document() or self.get_document() is None:
            self.timer.stop()
            self.pending.clear()
            return
        # Prioritize the viewport, then nearby pages in small batches so Qt
        # can handle input between renders. All PDF access stays on this thread.
        viewport = self.pages.viewport().rect()
        visible = [row for row, item in self.pending.items()
                   if self.pages.visualItemRect(item).intersects(viewport)]
        rows = visible[:4]
        if len(rows) < 4:
            rows += [row for row in self.pending if row not in rows][:4 - len(rows)]
        try:
            started = perf_counter()
            for row in rows:
                item = self.pending.pop(row)
                item.setIcon(self.render_icon(self.get_document()[row]))
                self.resident[row] = item
                if perf_counter() - started >= 0.016:
                    break
        except Exception as exc:
            self.timer.stop()
            self.pending.clear()
            self.on_error(exc)
        if not self.pending:
            self.timer.stop()
