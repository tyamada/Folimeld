import unittest
import json
from pathlib import Path

from folimeld.i18n import I18n


class SystemLanguageTests(unittest.TestCase):
    def test_windows_ui_language_is_japanese(self):
        self.assertEqual(I18n._system_language(), "ja")

    def test_all_languages_define_edit_labels(self):
        locales = Path(__file__).resolve().parent.parent / "locales"
        for path in locales.glob("*.json"):
            with self.subTest(language=path.stem):
                data = json.loads(path.read_text(encoding="utf-8"))
                self.assertTrue(data["insert_blank"])
                self.assertTrue(data["delete"])
                self.assertTrue(data["cannot_delete_all"])


if __name__ == "__main__":
    unittest.main()
