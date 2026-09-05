#!/usr/bin/env bash
set -eu

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

usage() {
  cat <<'EOF'
Usage: ./build_appstore.sh --application-identity IDENTITY --installer-identity IDENTITY --provisioning-profile PATH

Builds and signs a Mac App Store submission package.
EOF
}

APPLICATION_IDENTITY=""
INSTALLER_IDENTITY=""
PROVISIONING_PROFILE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --application-identity)
      [[ $# -ge 2 ]] || { echo "Missing value for --application-identity." >&2; exit 2; }
      APPLICATION_IDENTITY="$2"
      shift 2
      ;;
    --installer-identity)
      [[ $# -ge 2 ]] || { echo "Missing value for --installer-identity." >&2; exit 2; }
      INSTALLER_IDENTITY="$2"
      shift 2
      ;;
    --provisioning-profile)
      [[ $# -ge 2 ]] || { echo "Missing value for --provisioning-profile." >&2; exit 2; }
      PROVISIONING_PROFILE="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [[ -z "$APPLICATION_IDENTITY" || -z "$INSTALLER_IDENTITY" || -z "$PROVISIONING_PROFILE" ]]; then
  echo "Both signing identities and a provisioning profile are required." >&2
  usage >&2
  exit 2
fi

for command_name in codesign productbuild plutil pkgutil; do
  if ! command -v "$command_name" >/dev/null 2>&1; then
    echo "Required command not found: $command_name" >&2
    exit 1
  fi
done

ENTITLEMENTS="$SCRIPT_DIR/packaging/macos/Folimeld.entitlements"
[[ -f "$ENTITLEMENTS" ]] || { echo "Entitlements file not found: $ENTITLEMENTS" >&2; exit 1; }
[[ -f "$PROVISIONING_PROFILE" ]] || { echo "Provisioning profile not found: $PROVISIONING_PROFILE" >&2; exit 1; }

PYTHON_EXE="$SCRIPT_DIR/.venv/bin/python"
if [[ ! -x "$PYTHON_EXE" ]]; then
  echo "Python virtual environment was not found: $PYTHON_EXE" >&2
  echo "Run ./build_exe.sh first to create the build environment." >&2
  exit 1
fi

"$PYTHON_EXE" -m pip install -r requirements.txt pyinstaller
"$PYTHON_EXE" "$SCRIPT_DIR/tools/make_app_icon.py"

if ! command -v iconutil >/dev/null 2>&1; then
  echo "iconutil not found; cannot build the macOS icon." >&2
  exit 1
fi
iconutil -c icns "$SCRIPT_DIR/assets/Folimeld.iconset" -o "$SCRIPT_DIR/assets/Folimeld.icns"

rm -rf "$SCRIPT_DIR/build/Folimeld-mac" "$SCRIPT_DIR/dist/Folimeld.app"
"$PYTHON_EXE" -m PyInstaller \
  --noconfirm \
  --clean \
  --codesign-identity "$APPLICATION_IDENTITY" \
  --osx-entitlements-file "$ENTITLEMENTS" \
  Folimeld-mac.spec

APP_PATH="$SCRIPT_DIR/dist/Folimeld.app"
VERSION="$(/usr/libexec/PlistBuddy -c 'Print :CFBundleShortVersionString' "$APP_PATH/Contents/Info.plist")"
BUILD="$(/usr/libexec/PlistBuddy -c 'Print :CFBundleVersion' "$APP_PATH/Contents/Info.plist")"
PKG_PATH="$SCRIPT_DIR/dist/Folimeld_${VERSION}.pkg"

cp "$PROVISIONING_PROFILE" "$APP_PATH/Contents/embedded.provisionprofile"
codesign --force --deep --options runtime \
  --entitlements "$ENTITLEMENTS" \
  --sign "$APPLICATION_IDENTITY" "$APP_PATH"

codesign --verify --deep --strict --verbose=2 "$APP_PATH"
plutil -lint "$APP_PATH/Contents/Info.plist"

SIGNED_ENTITLEMENTS="$(mktemp -t folimeld-entitlements).plist"
trap 'rm -f "$SIGNED_ENTITLEMENTS"' EXIT
codesign --display --entitlements :- "$APP_PATH" > "$SIGNED_ENTITLEMENTS" 2>/dev/null

EXPECTED_BUNDLE_ID="com.folimeld.Folimeld"
ACTUAL_BUNDLE_ID="$(/usr/libexec/PlistBuddy -c 'Print :CFBundleIdentifier' "$APP_PATH/Contents/Info.plist")"
[[ "$ACTUAL_BUNDLE_ID" == "$EXPECTED_BUNDLE_ID" ]] || {
  echo "Unexpected bundle identifier: $ACTUAL_BUNDLE_ID" >&2
  exit 1
}
[[ "$VERSION" != "$BUILD" ]] || {
  echo "CFBundleShortVersionString and CFBundleVersion must be different values." >&2
  exit 1
}
[[ "$(/usr/libexec/PlistBuddy -c 'Print :CFBundleDocumentTypes:0:LSItemContentTypes:0' "$APP_PATH/Contents/Info.plist")" == "com.adobe.pdf" ]] || {
  echo "PDF document type is not registered." >&2
  exit 1
}
[[ "$(/usr/libexec/PlistBuddy -c 'Print :com.apple.security.app-sandbox' "$SIGNED_ENTITLEMENTS")" == "true" ]] || {
  echo "App Sandbox entitlement is missing or disabled." >&2
  exit 1
}
[[ "$(/usr/libexec/PlistBuddy -c 'Print :com.apple.security.files.user-selected.read-write' "$SIGNED_ENTITLEMENTS")" == "true" ]] || {
  echo "User-selected file read/write entitlement is missing or disabled." >&2
  exit 1
}

productbuild --component "$APP_PATH" /Applications \
  --sign "$INSTALLER_IDENTITY" "$PKG_PATH"

pkgutil --check-signature "$PKG_PATH"

echo
echo "Built: $PKG_PATH"
echo "Upload this package with Transporter or Xcode after TestFlight validation."
