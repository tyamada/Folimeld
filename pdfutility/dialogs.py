from PySide6.QtWidgets import (QCheckBox, QComboBox, QDialog, QDialogButtonBox,
                               QFormLayout, QLineEdit, QTabWidget, QVBoxLayout,
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
        for key, widget in (("pdf_version", self.pdf_version),
                            ("page_layout", self.page_layout),
                            ("cover_page", self.cover_page),
                            ("scroll_direction", self.scroll_direction)):
            details_form.addRow(tr(key), widget)
        tabs.addTab(summary, tr("summary")); tabs.addTab(details, tr("details"))
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept); buttons.rejected.connect(self.reject)
        layout_box = QVBoxLayout(self); layout_box.addWidget(tabs); layout_box.addWidget(buttons)

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
