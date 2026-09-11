import unittest

import fitz
from PySide6.QtWidgets import QApplication

from folimeld.dialogs import PropertiesDialog
from folimeld.i18n import I18n, LANGUAGES
from folimeld.model import PdfDocument


class DetailsTest(unittest.TestCase):
    def test_two_page_layout_raises_pdf_version_to_1_5(self) -> None:
        model = PdfDocument()
        model.doc = fitz.open()
        model.doc.new_page()
        self.addCleanup(model.close)

        model.set_details("1.4", "TwoPageLeft", False, False)

        self.assertEqual(model.doc.xref_get_key(model.doc.pdf_catalog(), "Version")[1], "/1.5")
        self.assertEqual(model.doc.pagelayout, "TwoPageLeft")

    def test_two_page_layout_preserves_pdf_version_above_1_5(self) -> None:
        model = PdfDocument()
        model.doc = fitz.open()
        model.doc.new_page()
        self.addCleanup(model.close)

        model.set_details("1.7", "TwoPageRight", True, False)

        self.assertEqual(model.doc.xref_get_key(model.doc.pdf_catalog(), "Version")[1], "/1.7")
        self.assertEqual(model.doc.pagelayout, "TwoPageRight")

    def test_other_layout_preserves_pdf_version_below_1_5(self) -> None:
        model = PdfDocument()
        model.doc = fitz.open()
        model.doc.new_page()
        self.addCleanup(model.close)

        model.set_details("1.4", "OneColumn", False, False)

        self.assertEqual(model.doc.xref_get_key(model.doc.pdf_catalog(), "Version")[1], "/1.4")
        self.assertEqual(model.doc.pagelayout, "OneColumn")


class PageDisplayTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.app = QApplication.instance() or QApplication([])

    def test_cover_notice_uses_real_translator_and_restores_display(self) -> None:
        model = PdfDocument()
        model.doc = fitz.open()
        model.doc.new_page()
        self.addCleanup(model.close)
        translator = I18n()
        for language in LANGUAGES:
            translator.load(language)
            dialog = PropertiesDialog(model, translator.tr)
            try:
                for layout, target in (("TwoColumnLeft", "TwoColumnRight"),
                                       ("TwoPageLeft", "TwoPageRight")):
                    with self.subTest(language=language, layout=layout):
                        dialog.page_layout.setCurrentText(layout)
                        baseline = dialog.page_display.text()
                        dialog.cover_page.setChecked(True)
                        self.assertIn(target, dialog.page_display.text())
                        self.assertIn("<b>", dialog.page_display.text())
                        self.assertNotIn("{layout}", dialog.page_display.text())
                        dialog.cover_page.setChecked(False)
                        self.assertEqual(dialog.page_display.text(), baseline)
            finally:
                dialog.reject()
                dialog.deleteLater()
