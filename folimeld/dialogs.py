from html import escape

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QCheckBox, QComboBox, QDialog, QDialogButtonBox,
                               QFormLayout, QLabel, QLineEdit, QTabWidget, QVBoxLayout,
                               QWidget)


class PropertiesDialog(QDialog):
    def __init__(self, model, tr, parent=None) -> None:
        super().__init__(parent)
        self.model, self.tr = model, tr
        self.setWindowTitle(tr("properties"))
        self.resize(500, 330)
        tabs = QTabWidget()
        summary = QWidget(); summary_form = QFormLayout(summary)
        metadata = model.doc.metadata
        filename = QLineEdit(model.path.name if model.path else "")
        filename.setReadOnly(True)
        self.title = QLineEdit(metadata.get("title", ""))
        self.author = QLineEdit(metadata.get("author", ""))
        self.subtitle = QLineEdit(metadata.get("subject", ""))
        self.keywords = QLineEdit(metadata.get("keywords", ""))
        for key, widget in (("filename", filename), ("title", self.title),
                            ("author", self.author), ("subtitle", self.subtitle),
                            ("keywords", self.keywords)):
            summary_form.addRow(tr(key), widget)
        details = QWidget(); details_form = QFormLayout(details)
        get_layout = getattr(model.doc, "get_pagelayout", None)
        if get_layout is None:
            get_layout = getattr(model.doc, "get_page_layout", None)
        page_layout = get_layout() if callable(get_layout) else getattr(model.doc, "pagelayout", "")
        version = metadata.get("format", "PDF 1.7").replace("PDF ", "")
        self.pdf_version = QComboBox()
        self.pdf_version.addItems(["1.0", "1.1", "1.2", "1.3", "1.4", "1.5", "1.6", "1.7", "2.0"])
        self.pdf_version.setCurrentText(version)
        self.page_layout = QComboBox()
        self.page_layout.addItems(["SinglePage", "OneColumn", "TwoColumnLeft",
                                   "TwoColumnRight", "TwoPageLeft", "TwoPageRight"])
        self.page_layout.setCurrentText(page_layout or "SinglePage")
        self.cover_page = QCheckBox(tr("yes"))
        self.cover_page.setChecked(page_layout == "TwoPageRight")
        self.scroll_direction = QComboBox()
        self.scroll_direction.addItem(tr("left_to_right"), False)
        self.scroll_direction.addItem(tr("right_to_left"), True)
        self.scroll_direction.setCurrentIndex(1 if self._is_right_to_left() else 0)
        self.page_display = QLabel()
        self.page_display.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.page_display.setTextFormat(Qt.TextFormat.RichText)
        self.page_display.setWordWrap(True)
        self.page_layout.currentTextChanged.connect(self._update_page_display)
        self.cover_page.toggled.connect(
            lambda _checked: self._update_page_display(self.page_layout.currentText())
        )
        self._update_page_display(self.page_layout.currentText())
        for key, widget in (("pdf_version", self.pdf_version),
                            ("page_layout", self.page_layout),
                            ("cover_page", self.cover_page),
                            ("scroll_direction", self.scroll_direction),
                            ("page_display", self.page_display)):
            details_form.addRow(tr(key), widget)
        page_display_label = details_form.labelForField(self.page_display)
        page_display_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        details_form.setAlignment(page_display_label, Qt.AlignmentFlag.AlignTop)
        tabs.addTab(summary, tr("summary")); tabs.addTab(details, tr("details"))
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept); buttons.rejected.connect(self.reject)
        layout_box = QVBoxLayout(self); layout_box.addWidget(tabs); layout_box.addWidget(buttons)

    def _update_page_display(self, page_layout: str) -> None:
        cover_layout = {
            "TwoColumnLeft": "TwoColumnRight", "TwoPageLeft": "TwoPageRight",
        }.get(page_layout) if self.cover_page.isChecked() else None
        descriptions = [self.tr("single_page_display" if page_layout in
                                ("SinglePage", "OneColumn") else "two_page_display")]
        if cover_layout or page_layout in ("TwoColumnRight", "TwoPageRight"):
            descriptions.append(self.tr("show_cover_page"))
        if page_layout in ("OneColumn", "TwoColumnLeft", "TwoColumnRight"):
            descriptions.append(self.tr("scrolling_enabled"))
        descriptions = [escape(text) for text in descriptions]
        if cover_layout:
            notice = self.tr("change_page_layout", layout=cover_layout)
            descriptions.append(f"<b>{escape(notice)}</b>")
        self.page_display.setText("<br>".join(descriptions))

    def _is_right_to_left(self) -> bool:
        catalog = self.model.doc.pdf_catalog()
        value_type, value = self.model.doc.xref_get_key(catalog, "ViewerPreferences")
        if value_type != "xref":
            return False
        preferences = int(value.split()[0])
        return self.model.doc.xref_get_key(preferences, "Direction")[1] == "/R2L"

    def accept(self) -> None:
        self.model.set_metadata(self.title.text(), self.author.text(), self.subtitle.text(), self.keywords.text())
        self.model.set_details(
            self.pdf_version.currentText(), self.page_layout.currentText(),
            self.cover_page.isChecked(), bool(self.scroll_direction.currentData()),
        )
        super().accept()
