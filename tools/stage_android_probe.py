"""Stage only the prototype and its shared model; never bundle user PDFs."""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]


def stage():
    target = ROOT / "build" / "android-probe"
    target.mkdir(parents=True, exist_ok=True)
    (target / "folimeld").mkdir(exist_ok=True)
    for name in ("__init__.py", "model.py", "android_probe.py"):
        shutil.copy2(ROOT / "folimeld" / name, target / "folimeld" / name)
    shutil.copy2(ROOT / "packaging/android/main.py", target / "main.py")
    shutil.copy2(ROOT / "LICENSE", target / "LICENSE")
    print(target)


if __name__ == "__main__":
    stage()
