from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QDragMoveEvent, QDropEvent
from PySide6.QtWidgets import QListWidget


class ThumbnailList(QListWidget):
    page_moved = Signal(int, int)

    def __init__(self) -> None:
        super().__init__()
        self.setViewMode(QListWidget.ViewMode.IconMode)
        self.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.setMovement(QListWidget.Movement.Snap)
        self.setWrapping(True)
        self.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        self.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.setIconSize(QSize(288, 288))
        self.setGridSize(QSize(312, 332))
        self.setSpacing(8)
        self._drag_row = -1

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

