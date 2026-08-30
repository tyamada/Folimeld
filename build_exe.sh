#!/usr/bin/env bash
set -eu

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

PYTHON_EXE="${SCRIPT_DIR}/.venv/bin/python"
if [ ! -x "$PYTHON_EXE" ]; then
  echo "Python virtual environment was not found: $PYTHON_EXE"
  echo "Create it with: python3 -m venv .venv"
  exit 1
fi

"$PYTHON_EXE" -m pip install -r requirements.txt pyinstaller
"$PYTHON_EXE" -m PyInstaller --noconfirm --clean Folimeld-mac.spec

echo

echo "Built: dist/Folimeld.app"
