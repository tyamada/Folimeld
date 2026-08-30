#!/usr/bin/env bash
set -eu

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

PYTHON_EXE="${SCRIPT_DIR}/.venv/bin/python"
if [ ! -x "$PYTHON_EXE" ]; then
  echo "Python virtual environment was not found: $PYTHON_EXE"
  echo "Creating it automatically..."
  python3 -m venv "$SCRIPT_DIR/.venv"
fi

if [ ! -x "$PYTHON_EXE" ]; then
  echo "Failed to create Python virtual environment: $PYTHON_EXE"
  exit 1
fi

"$PYTHON_EXE" -m pip install --upgrade pip
"$PYTHON_EXE" -m pip install -r requirements.txt pyinstaller
"$PYTHON_EXE" "$SCRIPT_DIR/tools/make_app_icon.py"

if command -v iconutil >/dev/null 2>&1; then
  iconutil -c icns "$SCRIPT_DIR/assets/Folimeld.iconset" -o "$SCRIPT_DIR/assets/Folimeld.icns"
else
  echo "iconutil not found; skipping ICNS generation."
fi

"$PYTHON_EXE" -m PyInstaller --noconfirm --clean Folimeld-mac.spec

if command -v codesign >/dev/null 2>&1; then
  echo "Ad-hoc signing the macOS app bundle..."
  xattr -cr "$SCRIPT_DIR/dist/Folimeld.app"
  codesign --force --deep --sign - "$SCRIPT_DIR/dist/Folimeld.app"
fi

echo

echo "Built: dist/Folimeld.app"
echo "Open the app bundle to run Folimeld on macOS."
