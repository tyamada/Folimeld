import json
import unittest
from unittest import mock
from pathlib import Path

from folimeld.i18n import (
    I18n,
    LANGUAGES,
    QT_LANGUAGE_CODES,
    STANDARD_BUTTON_LABELS,
    install_qt_translator,
    normalize_locale_code,
)


class SystemLanguageTests(unittest.TestCase):
    def test_system_language_is_a_supported_locale_code(self):
        self.assertIn(I18n._system_language(), LANGUAGES)

    def test_generic_locale_falls_back_to_english(self):
        with (mock.patch("folimeld.i18n.sys.platform", "linux"),
              mock.patch("folimeld.i18n.QLocale.system") as system):
            system.return_value.name.return_value = "C"
            self.assertEqual(I18n._system_language(), "en")

    def test_normalize_locale_code_routes_traditional_and_simplified_chinese(self):
        cases = [
            ("zh_TW", "zh_TW"),
            ("zh-TW", "zh_TW"),
            ("zh_HK", "zh_TW"),
            ("zh-HK", "zh_TW"),
            ("zh_MO", "zh_TW"),
            ("zh-Hant", "zh_TW"),
            ("zh-Hant-TW", "zh_TW"),
            ("zh_CN", "zh"),
            ("zh-CN", "zh"),
            ("zh_SG", "zh"),
            ("zh-Hans", "zh"),
            ("ko_KR", "ko"),
            ("ko-KR", "ko"),
            ("ja_JP", "ja"),
            ("en_US", "en"),
            ("pt_PT", "pt"),
            ("C", "en"),
            ("", "en"),
        ]
        for raw, expected in cases:
            with self.subTest(raw=raw):
                self.assertEqual(normalize_locale_code(raw), expected)

    def test_all_languages_define_edit_labels(self):
        locales = Path(__file__).resolve().parent.parent / "locales"
        for path in locales.glob("*.json"):
            with self.subTest(language=path.stem):
                data = json.loads(path.read_text(encoding="utf-8"))
                self.assertTrue(data["insert_blank"])
                self.assertTrue(data["delete"])
                self.assertTrue(data["cannot_delete_all"])

    def test_all_locales_are_complete(self):
        locales = Path(__file__).resolve().parent.parent / "locales"
        en = json.loads((locales / "en.json").read_text(encoding="utf-8"))
        ja = json.loads((locales / "ja.json").read_text(encoding="utf-8"))
        required = set(en) | set(ja)
        for code in LANGUAGES:
            with self.subTest(language=code):
                data = json.loads((locales / f"{code}.json").read_text(encoding="utf-8"))
                missing = sorted(required - set(data))
                self.assertEqual(missing, [])
                self.assertTrue(all(isinstance(v, str) and v.strip() for v in data.values()))

    def test_all_languages_define_standard_button_labels(self):
        self.assertEqual(set(STANDARD_BUTTON_LABELS), set(LANGUAGES))
        for language, labels in STANDARD_BUTTON_LABELS.items():
            with self.subTest(language=language):
                self.assertTrue(labels["discard"])
                self.assertTrue(labels["cancel"])

    def test_qt_translator_uses_qt_locale_aliases(self):
        app = mock.Mock()
        translator = mock.Mock()
        with (mock.patch("folimeld.i18n.QTranslator", return_value=translator),
              mock.patch("folimeld.i18n.QLibraryInfo.path", return_value="translations")):
            translator.load.return_value = True
            result = install_qt_translator(app, "zh")

        self.assertIs(result, translator)
        translator.load.assert_called_once_with(
            f"qtbase_{QT_LANGUAGE_CODES['zh']}", "translations",
        )
        app.installTranslator.assert_called_once_with(translator)


if __name__ == "__main__":
    unittest.main()
