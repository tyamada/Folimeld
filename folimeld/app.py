import sys
import logging
from pathlib import Path

from PySide6.QtCore import QSettings, QStandardPaths, QTimer, Qt
from PySide6.QtGui import QAction, QCloseEvent, QIcon, QKeySequence, QTransform
from PySide6.QtWidgets import (QApplication, QFileDialog, QMainWindow, QMessageBox,
                               QInputDialog, QLineEdit, QToolBar, QStyle)

from . import __version__
from .dialogs import PropertiesDialog
from .diagnostics import configure_logging
from .folder_dialog import select_image_folder
from .image_import import inventory
from .image_import_dialog import ImageImportDialog
from .help_dialog import HelpDialog
from .i18n import I18n, LANGUAGES, install_qt_translator
from .model import PasswordRequiredError, PdfDocument
from .pdf_save import save_with_progress
from .thumbnails import ThumbnailController
from .widgets import THUMBNAIL_SIZES, ThumbnailList
from .windows_integration import register_open_with, is_packaged
from .store_support import StoreSupport
from .support_dialog import SponsorsDialog, SupportDialog, supporter_icon
from .license_info import SOURCE_URL, license_documents


BUTTON_STYLES = {
    "icon_text": Qt.ToolButtonStyle.ToolButtonTextBesideIcon,
    "icon": Qt.ToolButtonStyle.ToolButtonIconOnly,
    "text": Qt.ToolButtonStyle.ToolButtonTextOnly,
}


class MainWindow(QMainWindow):
    def __init__(self, i18n: I18n | None = None) -> None:
        super().__init__()
        self.i18n = i18n or I18n()
        saved_style = QSettings().value("button_display", "text")
        self.button_display = saved_style if saved_style in BUTTON_STYLES else "text"
        self.model = PdfDocument()
        self._saving = False
        self.pages = ThumbnailList()
        self.thumbnails = ThumbnailController(
            self.pages, lambda: self.model.doc, lambda: self.thumbnail_size,
            lambda number: self.tr_("page", number=number), self.error,
        )
        try:
            size = int(QSettings().value("thumbnail_size", 288))
        except (TypeError, ValueError):
            size = 288
        self.thumbnail_size = size if size in THUMBNAIL_SIZES else 288
        self.pages.set_thumbnail_size(self.thumbnail_size)
        self.pages.page_moved.connect(self.reorder_page)
        self.setCentralWidget(self.pages)
        self.resize(1100, 760)
        self.support = StoreSupport(self) if is_packaged() else None
        self.support_dialog = None
        self.sponsors_dialog = None
        self.help_dialog = None
        self._build_ui()
        if self.support:
            self.support.changed.connect(self._update_support)
            QTimer.singleShot(0, self.support.refresh)
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
        self.undo_action = self._action("undo", self.undo)
        self.undo_action.setShortcuts(QKeySequence.StandardKey.Undo)
        self.redo_action = self._action("redo", self.redo)
        self.redo_action.setShortcuts(QKeySequence.StandardKey.Redo)
        edit_menu.addAction(self.undo_action)
        edit_menu.addAction(self.redo_action)
        edit_menu.addSeparator()
        self.insert_action = self._action("insert", self.insert_pdf, "Ctrl+I")
        self.insert_blank_action = self._action("insert_blank", self.insert_blank, "Ctrl+Shift+I")
        self.delete_action = self._action("delete", self.delete_selected, "Delete")
        self.properties_action = self._action("properties", self.properties)
        self.properties_action.setIconText(self.tr_("properties_short"))
        self.right_binding_action = self._action(
            "right_binding", lambda: self.set_right_binding(False))
        self.right_binding_cover_action = self._action(
            "right_binding_cover", lambda: self.set_right_binding(True))
        self.set_password_action = self._action("set_password", self.set_password)
        self.remove_password_action = self._action("remove_password", self.remove_password)
        for action in (self.open_action, self.save_action, self.save_as_action):
            file_menu.addAction(action)
        file_menu.addAction(self._action("import_images", self.import_image_folder))
        file_menu.addSeparator()
        file_menu.addAction(self.set_password_action)
        file_menu.addAction(self.remove_password_action)
        file_menu.addSeparator(); file_menu.addAction(self.properties_action)
        file_menu.addSeparator()
        self.exit_action = self._action("exit", self.close)
        self.exit_action.setShortcuts(QKeySequence.StandardKey.Quit)
        self.exit_action.setMenuRole(QAction.MenuRole.QuitRole)
        file_menu.addAction(self.exit_action)
        self.up_action = self._action("move_up", lambda: self.move(-1), "Alt+Up")
        self.down_action = self._action("move_down", lambda: self.move(1), "Alt+Down")
        self.left_action = self._action("rotate_left", lambda: self.rotate(-90), "Ctrl+Left")
        self.right_action = self._action("rotate_right", lambda: self.rotate(90), "Ctrl+Right")
        for action in (self.insert_action, self.insert_blank_action, self.delete_action,
                       self.up_action, self.down_action,
                       self.left_action, self.right_action):
            edit_menu.addAction(action)
        language_menu = settings_menu.addMenu(self.tr_("language"))
        settings_menu.addAction(self._action("image_size", self.change_image_size))
        settings_menu.addAction(self._action("button_display", self.change_button_display))
        for code, name in LANGUAGES.items():
            action = QAction(name, self); action.setCheckable(True)
            action.setChecked(code == self.i18n.language)
            action.triggered.connect(lambda checked=False, lang=code: self.change_language(lang))
            language_menu.addAction(action)
        self.help_action = self._action("help_usage", self.show_help, "F1")
        help_menu.addAction(self.help_action)
        help_menu.addSeparator()
        help_menu.addAction(self._action("version_info", self.about))
        help_menu.addAction(self._action("licenses", self.show_licenses))
        if self.support:
            self.support_action = self._action("support_title", self.show_support)
            self.support_action.setIconVisibleInMenu(True)
            help_menu.addAction(self.support_action)
        if sys.platform == "linux":
            self.sponsors_action = self._action("support_title", self.show_sponsors)
            help_menu.addAction(self.sponsors_action)
        toolbar = QToolBar(self.tr_("toolbar")); toolbar.setMovable(False)
        self.toolbar = toolbar
        toolbar.setToolButtonStyle(BUTTON_STYLES[self.button_display])
        icons = {
            "open": "SP_DialogOpenButton", "save": "SP_DialogSaveButton",
            "undo": "SP_ArrowBack", "redo": "SP_ArrowForward",
            "insert": "SP_FileDialogNewFolder", "insert_blank": "SP_FileIcon",
            "delete": "SP_TrashIcon", "move_up": "SP_ArrowUp",
            "move_down": "SP_ArrowDown", "rotate_left": "SP_BrowserReload",
            "rotate_right": "SP_BrowserReload", "properties": "SP_FileDialogDetailedView",
            "right_binding": "SP_ArrowLeft", "right_binding_cover": "SP_FileDialogContentsView",
        }
        for key, icon_name in icons.items():
            action = self.findChild(QAction, key)
            icon = self.style().standardIcon(getattr(QStyle.StandardPixmap, icon_name))
            if key == "rotate_left":
                icon = QIcon(icon.pixmap(32, 32).transformed(QTransform().scale(-1, 1)))
            action.setIcon(icon)
            action.setToolTip(action.text())
        self.addToolBar(toolbar)
        for action in (self.open_action, self.save_action, self.undo_action, self.redo_action, self.insert_action, self.insert_blank_action,
                       self.delete_action,
                       self.up_action,
                       self.down_action, self.left_action, self.right_action):
            toolbar.addAction(action)
        toolbar.addSeparator()
        for action in (self.properties_action, self.right_binding_action,
                       self.right_binding_cover_action):
            toolbar.addAction(action)
        self.statusBar().showMessage(self.tr_("ready"))

    def show_sponsors(self):
        if self.sponsors_dialog is None:
            self.sponsors_dialog = SponsorsDialog(self.tr_, self)
        self.sponsors_dialog.show()
        self.sponsors_dialog.raise_()
        self.sponsors_dialog.activateWindow()

    def _update_support(self):
        self.support_action.setText(self.tr_("supporter" if self.support.owned else "support_title"))
        self.support_action.setIcon(supporter_icon() if self.support.owned else QIcon())

    def show_support(self):
        if self.support_dialog is None:
            self.support_dialog = SupportDialog(self.support, self.tr_, self)
        self.support_dialog.show()
        self.support_dialog.raise_()
        self.support_dialog.activateWindow()
        self.support.refresh()

    def update_state(self) -> None:
        self.undo_action.setEnabled(self.model.can_undo)
        self.redo_action.setEnabled(self.model.can_redo)
        enabled = self.model.loaded
        for action in (self.save_action, self.save_as_action, self.insert_action,
                       self.properties_action, self.right_binding_action,
                       self.right_binding_cover_action, self.up_action, self.down_action,
                       self.left_action, self.right_action, self.set_password_action):
            action.setEnabled(enabled)
        self.insert_blank_action.setEnabled(enabled and bool(self.selected_rows()))
        self.delete_action.setEnabled(enabled and bool(self.selected_rows()))
        self.remove_password_action.setEnabled(enabled and self.model.password_protected)
        name = self.model.path.name if self.model.path else self.tr_("untitled")
        dirty = " *" if self.model.dirty else ""
        self.setWindowTitle(f"{name}{dirty} — {self.tr_('app_name')}")

    def confirm_discard(self) -> bool:
        if self._saving:
            return False
        if not self.model.dirty:
            return True
        dialog = QMessageBox(QMessageBox.Icon.Question, self.tr_("unsaved_title"),
                             self.tr_("unsaved_message"),
                             QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard |
                             QMessageBox.StandardButton.Cancel, self)
        for button, key in (
            (QMessageBox.StandardButton.Save, "save"),
            (QMessageBox.StandardButton.Discard, "discard"),
            (QMessageBox.StandardButton.Cancel, "cancel"),
        ):
            dialog.button(button).setText(self.tr_(key))
        answer = QMessageBox.StandardButton(dialog.exec())
        if answer == QMessageBox.StandardButton.Save:
            return self.save()
        return answer == QMessageBox.StandardButton.Discard

    def open_pdf(self) -> None:
        if not self.confirm_discard(): return
        path = self.select_pdf(self.tr_("open"))
        if not path: return
        self._open_path(path)

    def import_image_folder(self) -> None:
        settings = QSettings()
        initial = str(settings.value("last_image_directory", "") or "")
        if not Path(initial).is_dir():
            initial = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.PicturesLocation)
        folder = select_image_folder(self, self.tr_("import_images"), initial)
        if not folder:
            return
        settings.setValue("last_image_directory", folder)
        try:
            entries = inventory(folder)
            if not entries:
                QMessageBox.information(self, self.tr_("import_images"), self.tr_("image_empty"))
                return
            dialog = ImageImportDialog(entries, self.tr_, self)
            while dialog.exec():
                if not self.confirm_discard():
                    return
                if dialog.convert(self.model):
                    self.refresh()
                    return
        except Exception as exc:
            self.error(exc)

    def select_pdf(self, title: str) -> str:
        """Select a PDF, starting in and remembering the last-used folder."""
        settings = QSettings()
        saved_directory = str(settings.value("last_open_directory", "") or "")
        pictures_directory = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.PicturesLocation,
        )
        initial_directory = (
            saved_directory if Path(saved_directory).is_dir() else pictures_directory
        )
        path, _ = QFileDialog.getOpenFileName(
            self, title, initial_directory, "PDF (*.pdf)",
        )
        if path:
            settings.setValue("last_open_directory", str(Path(path).parent))
        return path

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
        path = self.select_pdf(self.tr_("insert"))
        if not path: return
        try:
            rows = self.selected_rows()
            self.model.insert(path, max(rows) if rows else None)
            self.refresh(preserve_scroll=True)
        except Exception as exc:
            self.error(exc)

    def insert_blank(self) -> None:
        try:
            rows = self.selected_rows()
            if rows:
                self.refresh(self.model.insert_blank_after(rows), preserve_scroll=True)
        except Exception as exc:
            self.error(exc)

    def delete_selected(self) -> None:
        try:
            rows = self.selected_rows()
            if rows:
                self.refresh(self.model.delete_pages(rows), preserve_scroll=True)
        except ValueError:
            QMessageBox.warning(self, self.tr_("delete"), self.tr_("cannot_delete_all"))
        except Exception as exc:
            self.error(exc)

    def change_button_display(self) -> None:
        modes = list(BUTTON_STYLES)
        choices = [self.tr_("button_display_" + mode) for mode in modes]
        choice, accepted = QInputDialog.getItem(
            self, self.tr_("button_display"), self.tr_("button_display"), choices,
            modes.index(self.button_display), False,
        )
        if accepted:
            self.button_display = modes[choices.index(choice)]
            self.toolbar.setToolButtonStyle(BUTTON_STYLES[self.button_display])
            QSettings().setValue("button_display", self.button_display)

    def change_image_size(self) -> None:
        choices = [f"{size} px" for size in THUMBNAIL_SIZES]
        choice, accepted = QInputDialog.getItem(
            self, self.tr_("image_size"), self.tr_("image_size"), choices,
            THUMBNAIL_SIZES.index(self.thumbnail_size), False,
        )
        if not accepted:
            return
        size = THUMBNAIL_SIZES[choices.index(choice)]
        if size == self.thumbnail_size:
            return
        selection = self.selected_rows()
        self.thumbnail_size = size
        self.pages.set_thumbnail_size(size)
        QSettings().setValue("thumbnail_size", size)
        self.refresh(selection, preserve_scroll=True)

    def refresh(self, selection: list[int] | None = None,
                preserve_scroll: bool = False) -> None:
        self.thumbnails.refresh(selection, preserve_scroll)
        self.update_state()
        self.statusBar().showMessage(self.tr_("pages_count", count=self.pages.count()))

    def selected_rows(self) -> list[int]:
        return sorted(self.pages.row(item) for item in self.pages.selectedItems())

    def undo(self) -> None:
        try:
            if self.model.undo():
                self.refresh(self.selected_rows(), preserve_scroll=True)
        except Exception as exc:
            self.error(exc)

    def redo(self) -> None:
        try:
            if self.model.redo():
                self.refresh(self.selected_rows(), preserve_scroll=True)
        except Exception as exc:
            self.error(exc)

    def reorder_page(self, old: int, new: int) -> None:
        try:
            self.model.reorder(old, new)
            self.refresh([new])
        except Exception as exc:
            self.refresh()
            self.error(exc)

    def move(self, direction: int) -> None:
        rows = self.selected_rows()
        try:
            if rows:
                self.refresh(self.model.move_selected(rows, direction))
        except Exception as exc:
            self.error(exc)

    def rotate(self, degrees: int) -> None:
        rows = self.selected_rows()
        try:
            self.model.rotate(rows, degrees)
            self.refresh(rows)
        except Exception as exc:
            self.error(exc)

    def save(self) -> bool:
        if not self.model.path: return self.save_as()
        return self._save_to(str(self.model.path))

    def save_as(self) -> bool:
        path, _ = QFileDialog.getSaveFileName(
            self, self.tr_("save_as"), str(self.model.path or ""), "PDF (*.pdf)",
        )
        return self._save_to(path) if path else False

    def _save_to(self, path: str) -> bool:
        if self._saving:
            return False
        self._saving = True
        self.thumbnails.pause()
        try:
            self.model.save(path, writer=lambda document, destination, options:
                            save_with_progress(document, destination, options, self, self.tr_("saving")))
            self.refresh(self.selected_rows(), preserve_scroll=True)
            self.statusBar().showMessage(self.tr_("saved"), 4000); return True
        except Exception as exc:
            self.error(exc); return False
        finally:
            self._saving = False
            self.thumbnails.resume()

    def properties(self) -> None:
        dialog = PropertiesDialog(self.model, self.tr_, self)
        accepted = dialog.exec()
        if self.thumbnails.document is not self.model.doc:
            self.refresh(self.selected_rows(), preserve_scroll=True)
        elif accepted:
            self.update_state()

    def set_right_binding(self, cover: bool) -> None:
        if not self.model.loaded:
            return
        try:
            version = self.model.doc.metadata.get("format", "PDF 1.7").replace("PDF ", "")
            kind, catalog_version = self.model.doc.xref_get_key(self.model.doc.pdf_catalog(), "Version")
            if kind == "name":
                version = catalog_version.removeprefix("/")
            self.model.set_details(
                version, "TwoPageRight" if cover else "TwoPageLeft", cover, True,
            )
            self.update_state()
        except Exception as exc:
            self.error(exc)

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
        try:
            self.model.set_view_password(password)
            self.update_state()
            self.statusBar().showMessage(self.tr_("password_set"), 4000)
        except Exception as exc:
            self.error(exc)

    def remove_password(self) -> None:
        answer = QMessageBox.question(
            self, self.tr_("remove_password"), self.tr_("remove_password_confirm"),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if answer == QMessageBox.StandardButton.Yes:
            try:
                self.model.set_view_password(None)
                self.update_state()
                self.statusBar().showMessage(self.tr_("password_removed"), 4000)
            except Exception as exc:
                self.error(exc)

    def change_language(self, language: str) -> None:
        QSettings().setValue("language", language)
        QMessageBox.information(self, self.tr_("language"), self.tr_("restart_required"))

    def show_help(self) -> None:
        if self.help_dialog is None:
            self.help_dialog = HelpDialog(self.tr_, (
                self.open_action, self.save_action, self.save_as_action,
                self.undo_action, self.redo_action,
                self.insert_action, self.insert_blank_action, self.delete_action,
                self.up_action, self.down_action, self.left_action,
                self.right_action, self.help_action,
            ), self)
        self.help_dialog.show()
        self.help_dialog.raise_()
        self.help_dialog.activateWindow()

    def about(self) -> None:
        text = self.tr_("version_text", version=__version__)
        text += "\n\nCopyright (C) 2026 Takuma Yamada"
        QMessageBox.about(self, self.tr_("version_info"), text)

    def show_licenses(self) -> None:
        from PySide6.QtWidgets import (QDialog, QDialogButtonBox, QLabel,
                                       QTabWidget, QTextBrowser, QVBoxLayout)

        dialog = QDialog(self)
        dialog.setWindowTitle(self.tr_("licenses"))
        dialog.resize(680, 520)
        layout = QVBoxLayout(dialog)
        layout.addWidget(QLabel("Folimeld\nCopyright (C) 2026 Takuma Yamada"))
        notice = QLabel(self.tr_("license_summary"))
        notice.setWordWrap(True)
        layout.addWidget(notice)
        source = QLabel(f'<a href="{SOURCE_URL}">{self.tr_("source_code")}</a>')
        source.setOpenExternalLinks(True)
        layout.addWidget(source)
        tabs = QTabWidget()
        for title, document in license_documents():
            browser = QTextBrowser()
            browser.setPlainText(document)
            tabs.addTab(browser, title)
        layout.addWidget(tabs)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        dialog.exec()

    def error(self, error: Exception) -> None:
        logging.getLogger(__name__).error('PDF operation failed',
                                         exc_info=(type(error), error, error.__traceback__))
        # Rollback replaces the PDF object; rebuild pending previews as well.
        if self.thumbnails.document is not self.model.doc:
            self.refresh(self.selected_rows(), preserve_scroll=True)
        QMessageBox.critical(self, self.tr_("error"), str(error))

    def closeEvent(self, event: QCloseEvent) -> None:
        if self.confirm_discard():
            self.thumbnails.clear()
            self.model.close(); event.accept()
        else: event.ignore()


def run() -> int:
    app = QApplication(sys.argv)
    app.setOrganizationName("Folimeld")
    app.setApplicationName("Folimeld")
    configure_logging(Path(QStandardPaths.writableLocation(
        QStandardPaths.StandardLocation.AppLocalDataLocation)) / 'logs')
    app.setDesktopFileName("folimeld")
    i18n = I18n()
    _qt_translator = install_qt_translator(app, i18n.language)
    resource_root = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent.parent))
    icon_path = resource_root / "assets" / "icon_256x256.png"
    if not icon_path.exists():
        icon_path = resource_root / "assets" / "Folimeld.iconset" / "icon_256x256.png"
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))
    try:
        register_open_with()
    except OSError:
        # Registry integration must never prevent the editor from starting.
        pass
    window = MainWindow(i18n); window.show()
    if len(sys.argv) > 1:
        path = sys.argv[1]
        QTimer.singleShot(0, lambda: window.open_path(path))
    return app.exec()

