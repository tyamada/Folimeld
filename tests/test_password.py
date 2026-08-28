import tempfile
import unittest
from pathlib import Path

import fitz

from pdfutility.model import PasswordRequiredError, PdfDocument


class PasswordTests(unittest.TestCase):
    def test_set_open_and_remove_viewing_password(self):
        with tempfile.TemporaryDirectory() as directory:
            plain = Path(directory) / "plain.pdf"
            protected = Path(directory) / "protected.pdf"
            unprotected = Path(directory) / "unprotected.pdf"
            source = fitz.open()
            source.new_page()
            source.save(plain)
            source.close()

            model = PdfDocument()
            model.open(str(plain))
            model.set_view_password("secret")
            model.save(str(protected))
            model.close()

            with self.assertRaises(PasswordRequiredError):
                model.open(str(protected), "wrong")
            model.open(str(protected), "secret")
            self.assertTrue(model.password_protected)
            model.set_view_password(None)
            model.save(str(unprotected))
            model.close()

            check = fitz.open(unprotected)
            self.assertFalse(check.needs_pass)
            check.close()


if __name__ == "__main__":
    unittest.main()
