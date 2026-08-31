import unittest

from folimeld.model import PdfDocument


class FakeDocument:
    def __init__(self) -> None:
        self.keys = {}
        self.layout = None

    def pdf_catalog(self) -> int:
        return 1

    def xref_set_key(self, xref: int, key: str, value: str) -> None:
        self.keys[(xref, key)] = value

    def xref_get_key(self, xref: int, key: str) -> tuple[str, str]:
        return ("xref", "2 0 R") if key == "ViewerPreferences" else ("null", "null")

    def set_pagelayout(self, layout: str) -> None:
        self.layout = layout


class DetailsTest(unittest.TestCase):
    def test_two_page_layout_raises_pdf_version_to_1_5(self) -> None:
        model = PdfDocument()
        model.doc = FakeDocument()

        model.set_details("1.4", "TwoPageLeft", False, False)

        self.assertEqual(model.doc.keys[(1, "Version")], "/1.5")
        self.assertEqual(model.doc.layout, "TwoPageLeft")

    def test_two_page_layout_preserves_pdf_version_above_1_5(self) -> None:
        model = PdfDocument()
        model.doc = FakeDocument()

        model.set_details("1.7", "TwoPageRight", True, False)

        self.assertEqual(model.doc.keys[(1, "Version")], "/1.7")
        self.assertEqual(model.doc.layout, "TwoPageRight")

    def test_other_layout_preserves_pdf_version_below_1_5(self) -> None:
        model = PdfDocument()
        model.doc = FakeDocument()

        model.set_details("1.4", "OneColumn", False, False)

        self.assertEqual(model.doc.keys[(1, "Version")], "/1.4")
        self.assertEqual(model.doc.layout, "OneColumn")
