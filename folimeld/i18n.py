import json
import locale
import sys
import ctypes

from .source_profile import application_settings

from PySide6.QtCore import QLibraryInfo, QLocale, QTranslator


LANGUAGES = {
    "ja": "日本語", "en": "English", "zh": "简体中文", "zh_TW": "繁體中文",
    "ko": "한국어", "de": "Deutsch", "fr": "Français", "es": "Español", "pt": "Português",
}

STANDARD_BUTTON_LABELS = {
    "ja": {"discard": "保存しない", "cancel": "キャンセル"},
    "en": {"discard": "Discard", "cancel": "Cancel"},
    "zh": {"discard": "不保存", "cancel": "取消"},
    "zh_TW": {"discard": "不儲存", "cancel": "取消"},
    "ko": {"discard": "저장 안 함", "cancel": "취소"},
    "de": {"discard": "Nicht speichern", "cancel": "Abbrechen"},
    "fr": {"discard": "Ne pas enregistrer", "cancel": "Annuler"},
    "es": {"discard": "No guardar", "cancel": "Cancelar"},
    "pt": {"discard": "Não guardar", "cancel": "Cancelar"},
}

QT_LANGUAGE_CODES = {"zh": "zh_CN", "zh_TW": "zh_TW", "pt": "pt_BR"}

TRADITIONAL_CHINESE_SUBTAGS = {"tw", "hk", "mo", "hant"}


def normalize_locale_code(raw: str) -> str:
    """Map an OS or Qt locale string (e.g. zh_TW, zh-HK, ko_KR) to a Folimeld language key."""
    if not raw:
        return "en"
    parts = [p.lower() for p in raw.replace("-", "_").split("_") if p]
    if not parts or parts[0] in {"c", "posix"}:
        return "en"
    if parts[0] == "zh":
        if any(sub in TRADITIONAL_CHINESE_SUBTAGS for sub in parts[1:]):
            return "zh_TW"
        return "zh"
    return parts[0]


def install_qt_translator(app, language: str) -> QTranslator:
    """Translate standard Qt widgets into the application's selected language."""
    translator = QTranslator(app)
    code = QT_LANGUAGE_CODES.get(language, language)
    translations = QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath)
    if translator.load(f"qtbase_{code}", translations):
        app.installTranslator(translator)
    return translator


class I18n:
    def __init__(self) -> None:
        settings = application_settings()
        saved = settings.value("language", "system")
        system = self._system_language()
        self.language = system if saved == "system" and system in LANGUAGES else saved
        if self.language not in LANGUAGES:
            self.language = "en"
        self._data: dict[str, str] = {}
        self.load(self.language)

    @staticmethod
    def _system_language() -> str:
        """Return the active UI language, falling back to English on generic locales."""
        if sys.platform == "win32":
            try:
                language_id = ctypes.windll.kernel32.GetUserDefaultUILanguage()
                windows_name = locale.windows_locale.get(language_id, "")
                if windows_name:
                    return normalize_locale_code(windows_name)
            except (AttributeError, OSError):
                pass

        return normalize_locale_code(QLocale.system().name())

    def load(self, language: str) -> None:
        from .resources import resource_root
        root = resource_root()
        path = root / "locales" / f"{language}.json"
        fallback = root / "locales" / "en.json"
        with fallback.open(encoding="utf-8") as handle:
            self._data = json.load(handle)
        if path != fallback and path.exists():
            with path.open(encoding="utf-8") as handle:
                self._data.update(json.load(handle))
        self._data.update(STANDARD_BUTTON_LABELS[language])
        self.language = language

    def tr(self, key: str, **values: object) -> str:
        return self._data.get(key, key).format(**values)
