import ctypes
import sys

from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QDragMoveEvent, QDropEvent, QFontMetrics, QWheelEvent
from PySide6.QtWidgets import QApplication, QAbstractItemView, QListWidget


SPI_GETWHEELSCROLLLINES = 0x0068
WHEEL_PAGESCROLL = 0xFFFFFFFF


def windows_wheel_scroll_lines() -> int | None:
    """Return the configured line count, or None for page scrolling."""
    value = ctypes.c_uint()
    try:
        success = ctypes.windll.user32.SystemParametersInfoW(
            SPI_GETWHEELSCROLLLINES, 0, ctypes.byref(value), 0,
        )
    except (AttributeError, OSError):
        return 3
    if not success:
        return 3
    return None if value.value == WHEEL_PAGESCROLL else value.value


class ThumbnailList(QListWidget):
    page_moved = Signal(int, int)

    def __init__(self) -> None:
        super().__init__()
        self.setViewMode(QListWidget.ViewMode.IconMode)
        self.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.setMovement(QListWidget.Movement.Snap)
        self.setWrapping(True)
        self.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        self.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.setIconSize(QSize(288, 288))
        self.setGridSize(QSize(312, 332))
        self.setSpacing(8)
        self._drag_row = -1
        self._wheel_angle_remainder = 0

    def wheelEvent(self, event: QWheelEvent) -> None:
        # Preserve Qt's smooth pixel scrolling for touchpads and the native
        # behavior on non-Windows platforms.
        angle_delta = event.angleDelta().y()
        if sys.platform != "win32" or not event.pixelDelta().isNull() or not angle_delta:
            super().wheelEvent(event)
            return

        self._wheel_angle_remainder += angle_delta
        steps = int(self._wheel_angle_remainder / 120)
        if not steps:
            event.accept()
            return
        self._wheel_angle_remainder -= steps * 120

        scroll_lines = windows_wheel_scroll_lines()
        scroll_bar = self.verticalScrollBar()
        if scroll_lines is None:
            amount = scroll_bar.pageStep()
        else:
            system_line_height = QFontMetrics(QApplication.font()).height()
            amount = scroll_lines * system_line_height
        scroll_bar.setValue(scroll_bar.value() - steps * amount)
        event.accept()

    def startDrag(self, supported_actions: Qt.DropAction) -> None:
        self._drag_row = self.currentRow()
        super().startDrag(supported_actions)

    def dragMoveEvent(self, event: QDragMoveEvent) -> None:
        event.setDropAction(Qt.DropAction.MoveAction)
        super().dragMoveEvent(event)

    def dropEvent(self, event: QDropEvent) -> None:
        old = self._drag_row
        pos = event.position().toPoint()
        target = self.indexAt(pos).row()
        if target < 0:
            target = self.count() - 1
        event.ignore()
        if old >= 0 and target >= 0 and old != target:
            self.page_moved.emit(old, target)
        self._drag_row = -1
