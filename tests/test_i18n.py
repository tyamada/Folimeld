import unittest
import json
from pathlib import Path

from folimeld.i18n import I18n, LANGUAGES


class SystemLanguageTests(unittest.TestCase):
    def test_system_language_is_a_supported_locale_code(self):
        self.assertIn(I18n._system_language(), LANGUAGES)

    def test_generic_locale_falls_back_to_english(self):
        with (unittest.mock.patch("folimeld.i18n.sys.platform", "linux"),
              unittest.mock.patch("folimeld.i18n.QLocale.system") as system):
            system.return_value.name.return_value = "C"
            self.assertEqual(I18n._system_language(), "en")

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
