import json
import locale
import sys
import ctypes
from pathlib import Path

from PySide6.QtCore import QLibraryInfo, QLocale, QSettings, QTranslator


LANGUAGES = {
    "ja": "日本語", "en": "English", "zh": "简体中文", "ko": "한국어",
    "de": "Deutsch", "fr": "Français", "es": "Español", "pt": "Português",
}

STANDARD_BUTTON_LABELS = {
    "ja": {"discard": "保存しない", "cancel": "キャンセル"},
    "en": {"discard": "Discard", "cancel": "Cancel"},
    "zh": {"discard": "不保存", "cancel": "取消"},
    "ko": {"discard": "저장 안 함", "cancel": "취소"},
    "de": {"discard": "Nicht speichern", "cancel": "Abbrechen"},
    "fr": {"discard": "Ne pas enregistrer", "cancel": "Annuler"},
    "es": {"discard": "No guardar", "cancel": "Cancelar"},
    "pt": {"discard": "Não guardar", "cancel": "Cancelar"},
}

QT_LANGUAGE_CODES = {"zh": "zh_CN", "pt": "pt_BR"}


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
        settings = QSettings()
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
                code = windows_name.split("_")[0].lower()
                if code and code not in {"c", "posix"}:
                    return code
            except (AttributeError, OSError):
                pass

        code = QLocale.system().name().split("_")[0].lower()
        if code and code not in {"c", "posix"}:
            return code
        return "en"

    def load(self, language: str) -> None:
        # PyInstaller extracts bundled data under _MEIPASS for one-file builds.
        root = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent.parent))
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
