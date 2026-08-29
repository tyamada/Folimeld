import unittest

from pdfutility.i18n import I18n


class SystemLanguageTests(unittest.TestCase):
    def test_windows_ui_language_is_japanese(self):
        self.assertEqual(I18n._system_language(), "ja")


if __name__ == "__main__":
    unittest.main()
