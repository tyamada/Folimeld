import json
import locale
import sys
from pathlib import Path

from PySide6.QtCore import QSettings


LANGUAGES = {
    "ja": "日本語", "en": "English", "zh": "简体中文", "ko": "한국어",
    "de": "Deutsch", "fr": "Français", "es": "Español", "pt": "Português",
}


class I18n:
    def __init__(self) -> None:
        settings = QSettings()
        saved = settings.value("language", "system")
        system = (locale.getlocale()[0] or "en").split("_")[0].lower()
        self.language = system if saved == "system" and system in LANGUAGES else saved
        if self.language not in LANGUAGES:
            self.language = "en"
        self._data: dict[str, str] = {}
        self.load(self.language)

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
        self.language = language

    def tr(self, key: str, **values: object) -> str:
        return self._data.get(key, key).format(**values)
