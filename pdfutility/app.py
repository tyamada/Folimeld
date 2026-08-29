import sys

import fitz
from PySide6.QtCore import QSettings, QTimer, Qt
from PySide6.QtGui import QAction, QCloseEvent, QIcon, QImage, QPixmap
from PySide6.QtWidgets import (QApplication, QFileDialog, QMainWindow, QMessageBox,
                               QInputDialog, QLineEdit, QToolBar, QListWidgetItem)

from . import __version__
from .dialogs import PropertiesDialog
from .i18n import I18n, LANGUAGES
from .model import PasswordRequiredError, PdfDocument
from .widgets import ThumbnailList
from .windows_integration import register_open_with


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.i18n = I18n()
        self.model = PdfDocument()
        self.pages = ThumbnailList()
        self.pages.page_moved.connect(self.reorder_page)
        self.setCentralWidget(self.pages)
        self.resize(1100, 760)
        self._build_ui()
        self.pages.itemSelectionChanged.connect(self.update_state)
        self.update_state()

    def tr_(self, key: str, **values: object) -> str:
        return self.i18n.tr(key, **values)

    def _action(self, key: str, slot, shortcut: str | None = None) -> QAction:
        action = QAction(self.tr_(key), self)
        action.triggered.connect(slot)
        if shortcut:
            action.setShortcut(shortcut)
        action.setObjectName(key)
        return action

    def _build_ui(self) -> None:
        self.setWindowTitle(self.tr_("app_name"))
        menu = self.menuBar(); menu.clear()
        file_menu = menu.addMenu(self.tr_("file"))
        edit_menu = menu.addMenu(self.tr_("edit"))
        settings_menu = menu.addMenu(self.tr_("settings"))
        help_menu = menu.addMenu(self.tr_("help"))
        self.open_action = self._action("open", self.open_pdf, "Ctrl+O")
        self.save_action = self._action("save", self.save, "Ctrl+S")
        self.save_as_action = self._action("save_as", self.save_as, "Ctrl+Shift+S")
        self.insert_action = self._action("insert", self.insert_pdf, "Ctrl+I")
        self.insert_blank_action = self._action("insert_blank", self.insert_blank, "Ctrl+Shift+I")
        self.delete_action = self._action("delete", self.delete_selected, "Delete")
        self.properties_action = self._action("properties", self.properties)
        self.set_password_action = self._action("set_password", self.set_password)
        self.remove_password_action = self._action("remove_password", self.remove_password)
        for action in (self.open_action, self.save_action, self.save_as_action):
            file_menu.addAction(action)
        file_menu.addSeparator()
        file_menu.addAction(self.set_password_action)
        file_menu.addAction(self.remove_password_action)
        file_menu.addSeparator(); file_menu.addAction(self.properties_action)
        self.up_action = self._action("move_up", lambda: self.move(-1), "Alt+Up")
        self.down_action = self._action("move_down", lambda: self.move(1), "Alt+Down")
        self.left_action = self._action("rotate_left", lambda: self.rotate(-90), "Ctrl+Left")
        self.right_action = self._action("rotate_right", lambda: self.rotate(90), "Ctrl+Right")
        for action in (self.insert_action, self.insert_blank_action, self.delete_action,
                       self.up_action, self.down_action,
                       self.left_action, self.right_action):
            edit_menu.addAction(action)
        language_menu = settings_menu.addMenu(self.tr_("language"))
        for code, name in LANGUAGES.items():
            action = QAction(name, self); action.setCheckable(True)
            action.setChecked(code == self.i18n.language)
            action.triggered.connect(lambda checked=False, lang=code: self.change_language(lang))
            language_menu.addAction(action)
        help_menu.addAction(self._action("version_info", self.about))
        toolbar = QToolBar(self.tr_("toolbar")); toolbar.setMovable(False)
        self.addToolBar(toolbar)
        for action in (self.open_action, self.save_action, self.insert_action, self.insert_blank_action,
                       self.delete_action,
                       self.up_action,
                       self.down_action, self.left_action, self.right_action):
            toolbar.addAction(action)
        self.statusBar().showMessage(self.tr_("ready"))

    def update_state(self) -> None:
        enabled = self.model.loaded
        for action in (self.save_action, self.save_as_action, self.insert_action,
                       self.properties_action, self.up_action, self.down_action,
                       self.left_action, self.right_action, self.set_password_action):
            action.setEnabled(enabled)
        self.insert_blank_action.setEnabled(enabled and bool(self.selected_rows()))
        self.delete_action.setEnabled(enabled and bool(self.selected_rows()))
        self.remove_password_action.setEnabled(enabled and self.model.password_protected)
        name = self.model.path.name if self.model.path else self.tr_("untitled")
        dirty = " *" if self.model.dirty else ""
        self.setWindowTitle(f"{name}{dirty} — {self.tr_('app_name')}")

    def confirm_discard(self) -> bool:
        if not self.model.dirty:
            return True
        answer = QMessageBox.question(self, self.tr_("unsaved_title"), self.tr_("unsaved_message"),
                                      QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard |
                                      QMessageBox.StandardButton.Cancel)
        if answer == QMessageBox.StandardButton.Save:
            return self.save()
        return answer == QMessageBox.StandardButton.Discard

    def open_pdf(self) -> None:
        if not self.confirm_discard(): return
        path, _ = QFileDialog.getOpenFileName(self, self.tr_("open"), "", "PDF (*.pdf)")
        if not path: return
        self._open_path(path)

    def open_path(self, path: str) -> None:
        """Open a PDF path supplied by Explorer or another external caller."""
        if self.confirm_discard():
            self._open_path(path)

    def _open_path(self, path: str) -> None:
        password = None
        while True:
            try:
                self.model.open(path, password); self.refresh(); return
            except PasswordRequiredError:
                password, accepted = QInputDialog.getText(
                    self, self.tr_("password_required"), self.tr_("enter_password"),
                    QLineEdit.EchoMode.Password,
                )
                if not accepted:
                    return
            except Exception as exc:
                self.error(exc); return

    def insert_pdf(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, self.tr_("insert"), "", "PDF (*.pdf)")
        if not path: return
        try:
            rows = self.selected_rows()
            self.model.insert(path, max(rows) if rows else None); self.refresh()
        except Exception as exc:
            self.error(exc)

    def insert_blank(self) -> None:
        try:
            rows = self.selected_rows()
            if rows:
                self.refresh(self.model.insert_blank_after(rows))
        except Exception as exc:
            self.error(exc)

    def delete_selected(self) -> None:
        try:
            rows = self.selected_rows()
            if rows:
                self.refresh(self.model.delete_pages(rows))
        except ValueError:
            QMessageBox.warning(self, self.tr_("delete"), self.tr_("cannot_delete_all"))
        except Exception as exc:
            self.error(exc)

    def render_icon(self, page: fitz.Page) -> QIcon:
        rect = page.rect
        scale = min(288 / rect.width, 288 / rect.height, 2.0)
        pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
        image = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format.Format_RGB888).copy()
        return QIcon(QPixmap.fromImage(image))

    def refresh(self, selection: list[int] | None = None) -> None:
        self.pages.clear()
        if self.model.doc:
            for index, page in enumerate(self.model.doc):
                item = QListWidgetItem(self.render_icon(page), self.tr_("page", number=index + 1))
                item.setTextAlignment(Qt.AlignmentFlag.AlignHCenter)
                item.setData(Qt.ItemDataRole.UserRole, index)
                self.pages.addItem(item)
            for row in selection or []:
                if 0 <= row < self.pages.count(): self.pages.item(row).setSelected(True)
        self.update_state()
        self.statusBar().showMessage(self.tr_("pages_count", count=self.pages.count()))

    def selected_rows(self) -> list[int]:
        return sorted(self.pages.row(item) for item in self.pages.selectedItems())

    def reorder_page(self, old: int, new: int) -> None:
        self.model.reorder(old, new); self.refresh([new])

    def move(self, direction: int) -> None:
        rows = self.selected_rows()
        if rows: self.refresh(self.model.move_selected(rows, direction))

    def rotate(self, degrees: int) -> None:
        rows = self.selected_rows()
        self.model.rotate(rows, degrees); self.refresh(rows)

    def save(self) -> bool:
        if not self.model.path: return self.save_as()
        return self._save_to(str(self.model.path))

    def save_as(self) -> bool:
        path, _ = QFileDialog.getSaveFileName(self, self.tr_("save_as"),
                                              str(self.model.path or ""), "PDF (*.pdf)")
        return self._save_to(path) if path else False

    def _save_to(self, path: str) -> bool:
        try:
            self.model.save(path); self.update_state()
            self.statusBar().showMessage(self.tr_("saved"), 4000); return True
        except Exception as exc:
            self.error(exc); return False

    def properties(self) -> None:
        dialog = PropertiesDialog(self.model, self.tr_, self)
        if dialog.exec(): self.update_state()

    def set_password(self) -> None:
        password, accepted = QInputDialog.getText(
            self, self.tr_("set_password"), self.tr_("new_password"),
            QLineEdit.EchoMode.Password,
        )
        if not accepted:
            return
        if not password:
            QMessageBox.warning(self, self.tr_("set_password"), self.tr_("password_empty"))
            return
        confirmation, accepted = QInputDialog.getText(
            self, self.tr_("set_password"), self.tr_("confirm_password"),
            QLineEdit.EchoMode.Password,
        )
        if not accepted:
            return
        if password != confirmation:
            QMessageBox.warning(self, self.tr_("set_password"), self.tr_("password_mismatch"))
            return
        self.model.set_view_password(password)
        self.update_state()
        self.statusBar().showMessage(self.tr_("password_set"), 4000)

    def remove_password(self) -> None:
        answer = QMessageBox.question(
            self, self.tr_("remove_password"), self.tr_("remove_password_confirm"),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if answer == QMessageBox.StandardButton.Yes:
            self.model.set_view_password(None)
            self.update_state()
            self.statusBar().showMessage(self.tr_("password_removed"), 4000)

    def change_language(self, language: str) -> None:
        QSettings().setValue("language", language)
        QMessageBox.information(self, self.tr_("language"), self.tr_("restart_required"))

    def about(self) -> None:
        QMessageBox.about(self, self.tr_("version_info"), self.tr_("version_text", version=__version__))

    def error(self, error: Exception) -> None:
        QMessageBox.critical(self, self.tr_("error"), str(error))

    def closeEvent(self, event: QCloseEvent) -> None:
        if self.confirm_discard():
            self.model.close(); event.accept()
        else: event.ignore()


def run() -> int:
    app = QApplication(sys.argv)
    app.setOrganizationName("PDFUtility")
    app.setApplicationName("PDF Utility")
    try:
        register_open_with()
    except OSError:
        # Registry integration must never prevent the editor from starting.
        pass
    window = MainWindow(); window.show()
    if len(sys.argv) > 1:
        path = sys.argv[1]
        QTimer.singleShot(0, lambda: window.open_path(path))
    return app.exec()

